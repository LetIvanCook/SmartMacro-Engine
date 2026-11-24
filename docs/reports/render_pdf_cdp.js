const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const http = require("http");

const htmlPath = path.resolve(process.argv[2]);
const pdfPath = path.resolve(process.argv[3]);
const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const port = 9229;
const userDataDir = path.join(path.dirname(htmlPath), "_chrome_cdp_profile");

function getJson(url) {
  return new Promise((resolve, reject) => {
    http
      .get(url, (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => resolve(JSON.parse(data)));
      })
      .on("error", reject);
  });
}

async function waitForCdp(retries = 30) {
  for (let i = 0; i < retries; i++) {
    try {
      const targets = await getJson(`http://127.0.0.1:${port}/json`);
      const page = targets.find((t) => t.type === "page");
      if (page && page.webSocketDebuggerUrl) return page.webSocketDebuggerUrl;
    } catch {}
    await new Promise((r) => setTimeout(r, 250));
  }
  throw new Error("Timed out waiting for Chrome CDP");
}

async function run() {
  fs.mkdirSync(userDataDir, { recursive: true });
  const chrome = spawn(
    chromePath,
    [
      "--headless=new",
      "--disable-gpu",
      "--no-sandbox",
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${userDataDir}`,
      "about:blank",
    ],
    { stdio: "ignore" }
  );

  try {
    const wsUrl = await waitForCdp();
    const ws = new WebSocket(wsUrl);
    await new Promise((resolve, reject) => {
      ws.onopen = resolve;
      ws.onerror = reject;
    });

    let msgId = 1;
    const send = (method, params = {}) =>
      new Promise((resolve, reject) => {
        const id = msgId++;
        const handler = (event) => {
          const msg = JSON.parse(event.data);
          if (msg.id === id) {
            ws.removeEventListener("message", handler);
            if (msg.error) reject(new Error(msg.error.message));
            else resolve(msg.result);
          }
        };
        ws.addEventListener("message", handler);
        ws.send(JSON.stringify({ id, method, params }));
      });

    await send("Page.enable");
    const fileUrl = "file:///" + htmlPath.replace(/\\/g, "/");
    const loadPromise = new Promise((resolve) => {
      const handler = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.method === "Page.loadEventFired") {
          ws.removeEventListener("message", handler);
          resolve();
        }
      };
      ws.addEventListener("message", handler);
    });

    await send("Page.navigate", { url: fileUrl });
    await loadPromise;
    await new Promise((r) => setTimeout(r, 400));

    const pdfResult = await send("Page.printToPDF", {
      printBackground: true,
      preferCSSPageSize: false,
      paperWidth: 8.27,
      paperHeight: 11.69,
      marginTop: 0.78,
      marginBottom: 0.78,
      marginLeft: 0.98,
      marginRight: 0.78,
      displayHeaderFooter: true,
      headerTemplate:
        '<div style="width:100%;font-size:8.5px;font-family:\'Times New Roman\',serif;color:#64748b;padding:0 22mm 0 26mm;display:flex;justify-content:space-between;border-bottom:0.5px solid #e2e8f0;padding-bottom:3px;"><span>Kế hoạch sử dụng AI — SmartMacro Engine</span><span>Khoa CNTT — ĐH Công nghệ Sài Gòn (STU)</span></div>',
      footerTemplate:
        '<div style="width:100%;font-size:8.5px;font-family:\'Times New Roman\',serif;color:#64748b;padding:0 22mm 0 26mm;display:flex;justify-content:space-between;"><span>Sinh viên: Lư Vĩnh An</span><span>Trang <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    });

    fs.writeFileSync(pdfPath, Buffer.from(pdfResult.data, "base64"));
    ws.close();
  } finally {
    chrome.kill("SIGTERM");
    setTimeout(() => {
      try {
        fs.rmSync(userDataDir, { recursive: true, force: true });
      } catch {}
    }, 500);
  }
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
