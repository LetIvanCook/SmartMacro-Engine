import { useAuth } from "../hooks/useAuth";
import { Button } from "../components/ui/button";
import { Dumbbell, LogOut, Sparkles, CheckCircle2, UserCheck, ShieldCheck } from "lucide-react";

export default function DashboardPlaceholderPage() {
  const { user, logout, isLoggingOut } = useAuth();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Navbar */}
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-md shadow-emerald-950/40">
              <Dumbbell className="h-5 w-5 text-slate-950 stroke-[2.5]" />
            </div>
            <div>
              <span className="font-bold text-lg text-white">SmartMacro</span>
              <span className="text-emerald-400 font-semibold ml-1 text-sm">Web</span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 text-sm text-slate-300 bg-slate-800/60 py-1.5 px-3 rounded-full border border-slate-700/50">
              <UserCheck className="h-4 w-4 text-emerald-400" />
              <span>{user?.fullName || user?.email || "Người dùng"}</span>
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={() => logout()}
              disabled={isLoggingOut}
              className="gap-2 border-slate-700 text-slate-300 hover:text-red-400 hover:border-red-800/60"
            >
              <LogOut className="h-4 w-4" />
              <span>{isLoggingOut ? "Đang thoát..." : "Đăng xuất"}</span>
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-4xl mx-auto px-4 py-12 flex flex-col items-center justify-center text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-700/50 text-emerald-300 text-xs font-semibold uppercase tracking-wider mb-6">
          <ShieldCheck className="h-4 w-4" />
          <span>Sprint 1 — Protected Route Active</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-extrabold text-white mb-4">
          Chào mừng, <span className="text-emerald-400">{user?.fullName || "Bạn"}</span>!
        </h1>

        <p className="text-slate-400 text-base max-w-xl mb-8 leading-relaxed">
          Bạn đã đăng nhập thành công vào phiên làm việc bảo mật. Hệ thống đã lưu trữ session và kích hoạt cơ chế <strong>Silent Token Refresh</strong>.
        </p>

        {/* Milestone Card */}
        <div className="w-full max-w-2xl bg-slate-900/80 border border-slate-800 rounded-2xl p-6 sm:p-8 text-left shadow-xl mb-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400">
              <Sparkles className="h-6 w-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Lộ Trình Tính Năng Kế Tiếp</h2>
              <p className="text-xs text-slate-400">Giao diện Dashboard tổng hợp & Solver sẽ xuất hiện tại đây</p>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            <div className="flex items-start gap-3 p-3 rounded-lg bg-emerald-950/20 border border-emerald-800/30">
              <CheckCircle2 className="h-5 w-5 text-emerald-400 mt-0.5 shrink-0" />
              <div>
                <p className="text-sm font-semibold text-emerald-200">Sprint 1: Scaffolding & Auth Flow (Hoàn tất)</p>
                <p className="text-xs text-slate-400">React 19, TypeScript, Tailwind CSS, Shadcn UI, Zustand, Axios Silent Token Refresh.</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-lg bg-slate-800/40 border border-slate-700/40 opacity-80">
              <div className="h-5 w-5 rounded-full border-2 border-slate-500 mt-0.5 shrink-0 flex items-center justify-center text-[10px] font-bold text-slate-400">2</div>
              <div>
                <p className="text-sm font-medium text-slate-200">Sprint 2: Food Catalog & Kho Thực Phẩm (Inventory)</p>
                <p className="text-xs text-slate-400">Quản lý tủ lạnh, số gram tồn kho, phân loại nhóm thực phẩm.</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-lg bg-slate-800/40 border border-slate-700/40 opacity-80">
              <div className="h-5 w-5 rounded-full border-2 border-slate-500 mt-0.5 shrink-0 flex items-center justify-center text-[10px] font-bold text-slate-400">3</div>
              <div>
                <p className="text-sm font-medium text-slate-200">Sprint 3: Daily Targets & Chu Kỳ Tập Luyện</p>
                <p className="text-xs text-slate-400">Thiết lập mục tiêu Macro & Calo thích ứng theo lịch tập Push/Pull/Legs/Rest.</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-lg bg-slate-800/40 border border-slate-700/40 opacity-80">
              <div className="h-5 w-5 rounded-full border-2 border-slate-500 mt-0.5 shrink-0 flex items-center justify-center text-[10px] font-bold text-slate-400">4</div>
              <div>
                <p className="text-sm font-medium text-slate-200">Sprint 4: Flagship Optimization Dashboard</p>
                <p className="text-xs text-slate-400">Vòng tròn Macro Rings, 1-click OR-Tools Linear Programming Solver.</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

