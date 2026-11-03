import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { macroApi } from "../api/macro.api";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import type {
  DailyTargetResponseDto,
  FoodResponseDto,
  InventoryItemResponseDto,
  OptimizationResultDto,
  UserDashboardResponseDto,
} from "../types/macro.types";
import {
  Calculator,
  CheckCircle2,
  Database,
  Dumbbell,
  Flame,
  LogOut,
  PackagePlus,
  PlusCircle,
  Refrigerator,
  Target,
  Trash2,
  UserCheck,
} from "lucide-react";

type ActiveTab = "dashboard" | "inventory" | "optimizer";

// Danh sách 5 món ăn mẫu quen thuộc dùng cho nút "Nạp dữ liệu mẫu (Demo Seed)"
const DEMO_FOODS_SEED = [
  {
    foodName: "Ức gà phi lê",
    kcalPer100g: 165,
    proteinGPer100g: 31,
    carbsGPer100g: 0,
    fatGPer100g: 3.6,
    defaultGrams: 600,
    daysToExpiry: 5,
  },
  {
    foodName: "Cơm trắng",
    kcalPer100g: 130,
    proteinGPer100g: 2.7,
    carbsGPer100g: 28,
    fatGPer100g: 0.3,
    defaultGrams: 800,
    daysToExpiry: 2,
  },
  {
    foodName: "Trứng gà nguyên quả",
    kcalPer100g: 155,
    proteinGPer100g: 13,
    carbsGPer100g: 1.1,
    fatGPer100g: 11,
    defaultGrams: 500,
    daysToExpiry: 10,
  },
  {
    foodName: "Khoai lang luộc",
    kcalPer100g: 86,
    proteinGPer100g: 1.6,
    carbsGPer100g: 20,
    fatGPer100g: 0.1,
    defaultGrams: 600,
    daysToExpiry: 7,
  },
  {
    foodName: "Bông cải xanh (Súp lơ xanh)",
    kcalPer100g: 34,
    proteinGPer100g: 2.8,
    carbsGPer100g: 7,
    fatGPer100g: 0.4,
    defaultGrams: 400,
    daysToExpiry: 4,
  },
];

function getFutureDateString(daysAhead: number): string {
  const date = new Date();
  date.setDate(date.getDate() + daysAhead);
  return date.toISOString().split("T")[0];
}

export default function DashboardPlaceholderPage() {
  const { user, logout, isLoggingOut } = useAuth();

  // State điều hướng 3 màn hình chính
  const [activeTab, setActiveTab] = useState<ActiveTab>("dashboard");

  // State dữ liệu từ Backend API
  const [dashboardSummary, setDashboardSummary] =
    useState<UserDashboardResponseDto | null>(null);
  const [todayTarget, setTodayTarget] = useState<DailyTargetResponseDto | null>(null);
  const [inventory, setInventory] = useState<InventoryItemResponseDto[]>([]);
  const [foods, setFoods] = useState<FoodResponseDto[]>([]);
  const [optimizationResult, setOptimizationResult] =
    useState<OptimizationResultDto | null>(null);

  // State thông báo & trạng thái tải
  const [isLoadingData, setIsLoadingData] = useState<boolean>(true);
  const [isSeeding, setIsSeeding] = useState<boolean>(false);
  const [isSavingTarget, setIsSavingTarget] = useState<boolean>(false);
  const [isAddingInventory, setIsAddingInventory] = useState<boolean>(false);
  const [isCreatingFood, setIsCreatingFood] = useState<boolean>(false);
  const [isOptimizing, setIsOptimizing] = useState<boolean>(false);
  const [statusMessage, setStatusMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  // State Form Màn hình 1: Nhập / Cập nhật Mục tiêu Macro trong ngày
  const [targetKcal, setTargetKcal] = useState<string>("2200");
  const [targetProteinG, setTargetProteinG] = useState<string>("160");
  const [targetCarbsG, setTargetCarbsG] = useState<string>("250");
  const [targetFatG, setTargetFatG] = useState<string>("60");

  // State Form Màn hình 2: Thêm nhanh thực phẩm vào kho tủ lạnh
  const [selectedFoodId, setSelectedFoodId] = useState<string>("");
  const [quantityGrams, setQuantityGrams] = useState<string>("500");
  const [expiryDate, setExpiryDate] = useState<string>(() => getFutureDateString(5));

  // State Form phụ: Thêm món ăn mới vào danh mục hệ thống (/api/foods)
  const [newFoodName, setNewFoodName] = useState<string>("");
  const [newFoodKcal, setNewFoodKcal] = useState<string>("");
  const [newFoodProtein, setNewFoodProtein] = useState<string>("");
  const [newFoodCarbs, setNewFoodCarbs] = useState<string>("");
  const [newFoodFat, setNewFoodFat] = useState<string>("");

  // Hàm tải toàn bộ dữ liệu từ các API Backend
  const reloadAllData = async () => {
    try {
      const [summaryRes, todayRes, invRes, foodsRes] = await Promise.all([
        macroApi.getDashboardSummary(),
        macroApi.getTodayTarget(),
        macroApi.getInventory(),
        macroApi.getFoods("", 100),
      ]);

      setDashboardSummary(summaryRes);
      setTodayTarget(todayRes);
      setInventory(invRes);
      setFoods(foodsRes.items);

      if (todayRes) {
        setTargetKcal(String(todayRes.targetKcal));
        setTargetProteinG(String(todayRes.targetProteinG));
        setTargetCarbsG(String(todayRes.targetCarbsG));
        setTargetFatG(String(todayRes.targetFatG));
      } else if (summaryRes?.todayTarget) {
        setTargetKcal(String(summaryRes.todayTarget.targetKcal));
        setTargetProteinG(String(summaryRes.todayTarget.targetProteinG));
        setTargetCarbsG(String(summaryRes.todayTarget.targetCarbsG));
        setTargetFatG(String(summaryRes.todayTarget.targetFatG));
      }

      if (foodsRes.items.length > 0) {
        setSelectedFoodId((prev) => prev || String(foodsRes.items[0].foodId));
      }
    } catch {
      setStatusMessage({
        type: "error",
        text: "Không thể tải dữ liệu từ Backend API. Hãy kiểm tra Backend đã bật chưa.",
      });
    } finally {
      setIsLoadingData(false);
    }
  };

  useEffect(() => {
    let ignore = false;
    void (async () => {
      try {
        const [summaryRes, todayRes, invRes, foodsRes] = await Promise.all([
          macroApi.getDashboardSummary(),
          macroApi.getTodayTarget(),
          macroApi.getInventory(),
          macroApi.getFoods("", 100),
        ]);
        if (ignore) return;

        setDashboardSummary(summaryRes);
        setTodayTarget(todayRes);
        setInventory(invRes);
        setFoods(foodsRes.items);

        if (todayRes) {
          setTargetKcal(String(todayRes.targetKcal));
          setTargetProteinG(String(todayRes.targetProteinG));
          setTargetCarbsG(String(todayRes.targetCarbsG));
          setTargetFatG(String(todayRes.targetFatG));
        } else if (summaryRes?.todayTarget) {
          setTargetKcal(String(summaryRes.todayTarget.targetKcal));
          setTargetProteinG(String(summaryRes.todayTarget.targetProteinG));
          setTargetCarbsG(String(summaryRes.todayTarget.targetCarbsG));
          setTargetFatG(String(summaryRes.todayTarget.targetFatG));
        }

        if (foodsRes.items.length > 0) {
          setSelectedFoodId((prev) => prev || String(foodsRes.items[0].foodId));
        }
      } catch {
        if (!ignore) {
          setStatusMessage({
            type: "error",
            text: "Không thể tải dữ liệu từ Backend API. Hãy kiểm tra Backend đã bật chưa.",
          });
        }
      } finally {
        if (!ignore) {
          setIsLoadingData(false);
        }
      }
    })();

    return () => {
      ignore = true;
    };
  }, []);

  // Xử lý lưu / cập nhật mục tiêu Macro hôm nay (POST hoặc PUT /api/daily-targets)
  const handleSaveDailyTarget = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSavingTarget(true);
    setStatusMessage(null);

    const payload = {
      targetKcal: Number(targetKcal),
      targetProteinG: Number(targetProteinG),
      targetCarbsG: Number(targetCarbsG),
      targetFatG: Number(targetFatG),
    };

    try {
      let saved: DailyTargetResponseDto;
      if (todayTarget && todayTarget.id) {
        saved = await macroApi.updateDailyTarget(todayTarget.id, payload);
      } else {
        saved = await macroApi.createDailyTarget(payload);
      }
      setTodayTarget(saved);
      const summary = await macroApi.getDashboardSummary();
      setDashboardSummary(summary);
      setStatusMessage({
        type: "success",
        text: `Đã lưu mục tiêu hôm nay: ${saved.targetKcal} kcal (${saved.targetProteinG}g P / ${saved.targetCarbsG}g C / ${saved.targetFatG}g F).`,
      });
    } catch {
      setStatusMessage({
        type: "error",
        text: "Lỗi khi lưu mục tiêu. Vui lòng kiểm tra các chỉ số lớn hơn 0.",
      });
    } finally {
      setIsSavingTarget(false);
    }
  };

  // Xử lý thêm thực phẩm từ danh sách vào kho tủ lạnh cá nhân (POST /api/inventory)
  const handleAddInventoryItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFoodId) return;

    setIsAddingInventory(true);
    setStatusMessage(null);

    try {
      await macroApi.addInventoryItem({
        foodId: Number(selectedFoodId),
        quantityGrams: Number(quantityGrams),
        expiryDate: expiryDate || null,
      });

      const [updatedInventory, updatedSummary] = await Promise.all([
        macroApi.getInventory(),
        macroApi.getDashboardSummary(),
      ]);
      setInventory(updatedInventory);
      setDashboardSummary(updatedSummary);
      setStatusMessage({
        type: "success",
        text: "Đã thêm thực phẩm vào kho tủ lạnh cá nhân thành công!",
      });
    } catch {
      setStatusMessage({
        type: "error",
        text: "Không thể thêm vào kho. Hãy kiểm tra khối lượng (gram > 0) và hạn sử dụng.",
      });
    } finally {
      setIsAddingInventory(false);
    }
  };

  // Xử lý xóa 1 thực phẩm khỏi tủ lạnh (DELETE /api/inventory/{id})
  const handleDeleteInventoryItem = async (inventoryId: number) => {
    setStatusMessage(null);
    try {
      await macroApi.deleteInventoryItem(inventoryId);
      const [updatedInventory, updatedSummary] = await Promise.all([
        macroApi.getInventory(),
        macroApi.getDashboardSummary(),
      ]);
      setInventory(updatedInventory);
      setDashboardSummary(updatedSummary);
      setStatusMessage({
        type: "success",
        text: "Đã xóa nguyên liệu khỏi tủ lạnh.",
      });
    } catch {
      setStatusMessage({
        type: "error",
        text: "Lỗi khi xóa nguyên liệu khỏi kho.",
      });
    }
  };

  // Xử lý tạo thêm món ăn mới vào danh mục (/api/foods)
  const handleCreateFood = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFoodName.trim()) return;

    setIsCreatingFood(true);
    setStatusMessage(null);

    try {
      const created = await macroApi.createFood({
        foodName: newFoodName.trim(),
        kcalPer100g: Number(newFoodKcal),
        proteinGPer100g: Number(newFoodProtein),
        carbsGPer100g: Number(newFoodCarbs),
        fatGPer100g: Number(newFoodFat),
      });

      const foodsRes = await macroApi.getFoods("", 100);
      setFoods(foodsRes.items);
      setSelectedFoodId(String(created.foodId));
      setNewFoodName("");
      setNewFoodKcal("");
      setNewFoodProtein("");
      setNewFoodCarbs("");
      setNewFoodFat("");
      setStatusMessage({
        type: "success",
        text: `Đã thêm món "${created.foodName}" vào danh sách món ăn hệ thống!`,
      });
    } catch {
      setStatusMessage({
        type: "error",
        text: "Không thể tạo món ăn mới. Vui lòng kiểm tra thông tin nhập.",
      });
    } finally {
      setIsCreatingFood(false);
    }
  };

  // Xử lý gọi thuật toán Quy hoạch tuyến tính Google OR-Tools (POST /api/optimizations/generate-plan)
  const handleGenerateOptimalPlan = async () => {
    setIsOptimizing(true);
    setStatusMessage(null);

    try {
      const result = await macroApi.generateMealPlan({
        dailyTargetId: todayTarget?.id ?? null,
      });
      setOptimizationResult(result);
      setActiveTab("optimizer");
      setStatusMessage({
        type: result.solverStatus === "INFEASIBLE" ? "error" : "success",
        text:
          result.solverStatus === "INFEASIBLE"
            ? "Kho thực phẩm hiện tại chưa đủ nguyên liệu để ghép đạt mục tiêu ±5%. Hãy nạp thêm thực phẩm!"
            : `Bộ giải OR-Tools (${result.solverStatus}) đã tìm ra khẩu phần ăn tối ưu!`,
      });
    } catch {
      setStatusMessage({
        type: "error",
        text: "Chưa thể tính toán thực đơn. Hãy đảm bảo bạn đã Đặt mục tiêu hôm nay và Kho tủ lạnh có thực phẩm (hoặc bấm nút Nạp dữ liệu mẫu).",
      });
    } finally {
      setIsOptimizing(false);
    }
  };

  // Nút "Nạp dữ liệu mẫu (Demo Seed)": Tạo 5 món quen thuộc + Nạp vào tủ lạnh + Đặt mục tiêu 2200 kcal
  const handleDemoSeed = async () => {
    setIsSeeding(true);
    setStatusMessage(null);

    try {
      // Bước 1: Kiểm tra danh sách món ăn hiện có
      const existingFoodsPage = await macroApi.getFoods("", 100);
      const currentFoods = [...existingFoodsPage.items];

      // Bước 2: Tạo các món mẫu nếu chưa có và thêm vào tủ lạnh cá nhân
      for (const sample of DEMO_FOODS_SEED) {
        let matched = currentFoods.find(
          (f) => f.foodName.toLowerCase() === sample.foodName.toLowerCase()
        );

        if (!matched) {
          matched = await macroApi.createFood({
            foodName: sample.foodName,
            kcalPer100g: sample.kcalPer100g,
            proteinGPer100g: sample.proteinGPer100g,
            carbsGPer100g: sample.carbsGPer100g,
            fatGPer100g: sample.fatGPer100g,
          });
          currentFoods.push(matched);
        }

        await macroApi.addInventoryItem({
          foodId: matched.foodId,
          quantityGrams: sample.defaultGrams,
          expiryDate: getFutureDateString(sample.daysToExpiry),
        });
      }

      // Bước 3: Đặt mục tiêu mẫu (2200 kcal, 160g Protein, 250g Carb, 60g Fat)
      const demoTargetPayload = {
        targetKcal: 2200,
        targetProteinG: 160,
        targetCarbsG: 250,
        targetFatG: 60,
      };

      const currentTodayTarget = await macroApi.getTodayTarget();
      if (currentTodayTarget && currentTodayTarget.id) {
        await macroApi.updateDailyTarget(currentTodayTarget.id, demoTargetPayload);
      } else {
        await macroApi.createDailyTarget(demoTargetPayload);
      }

      // Bước 4: Tải lại dữ liệu mới nhất lên giao diện
      await reloadAllData();

      setStatusMessage({
        type: "success",
        text: "Đã nạp dữ liệu mẫu thành công! (5 món: Ức gà, Cơm trắng, Trứng gà, Khoai lang, Bông cải xanh + Mục tiêu 2200 kcal). Bạn có thể bấm 'Tính toán khẩu phần ăn tối ưu' ngay!",
      });
    } catch {
      setStatusMessage({
        type: "error",
        text: "Có lỗi xảy ra khi nạp dữ liệu mẫu. Vui lòng thử lại.",
      });
    } finally {
      setIsSeeding(false);
    }
  };

  const activeTarget = todayTarget ?? dashboardSummary?.todayTarget ?? null;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Thanh Header trên cùng */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between gap-2">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-md">
              <Dumbbell className="h-5 w-5 text-slate-950 stroke-[2.5]" />
            </div>
            <div>
              <span className="font-bold text-lg text-white">SmartMacro</span>
              <span className="text-emerald-400 font-semibold ml-1 text-sm">
                Engine
              </span>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                Hệ thống quản lý kho thực phẩm &amp; tối ưu thực đơn bằng OR-Tools
              </p>
            </div>
          </div>

          {/* Nút Nạp dữ liệu mẫu (Demo Seed) & Thông tin User trên góc giao diện */}
          <div className="flex items-center gap-2 sm:gap-3">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => void handleDemoSeed()}
              disabled={isSeeding}
              className="gap-1.5 bg-amber-500/15 text-amber-300 border border-amber-500/40 hover:bg-amber-500/25"
            >
              <Database className="h-4 w-4 text-amber-400" />
              <span>
                {isSeeding ? "Đang nạp mẫu..." : "Nạp dữ liệu mẫu (Demo Seed)"}
              </span>
            </Button>

            <div className="hidden md:flex items-center gap-2 text-xs text-slate-300 bg-slate-800/70 py-1.5 px-3 rounded-full border border-slate-700">
              <UserCheck className="h-3.5 w-3.5 text-emerald-400" />
              <span>{user?.fullName || user?.email || "Hội viên"}</span>
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={() => void logout()}
              disabled={isLoggingOut}
              className="gap-1.5 border-slate-700 text-slate-300 hover:text-red-400"
            >
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">
                {isLoggingOut ? "Đang thoát..." : "Đăng xuất"}
              </span>
            </Button>
          </div>
        </div>
      </header>

      {/* Nội dung chính */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 py-6">
        {/* Thanh chuyển đổi 3 màn hình cốt lõi */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 mb-6 bg-slate-900/90 p-1.5 rounded-xl border border-slate-800">
          <button
            type="button"
            onClick={() => setActiveTab("dashboard")}
            className={`flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-sm font-semibold transition-colors cursor-pointer ${
              activeTab === "dashboard"
                ? "bg-emerald-600 text-white shadow"
                : "text-slate-400 hover:text-white hover:bg-slate-800/60"
            }`}
          >
            <Target className="h-4 w-4" />
            <span>1. Tổng quan &amp; Mục tiêu</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("inventory")}
            className={`flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-sm font-semibold transition-colors cursor-pointer ${
              activeTab === "inventory"
                ? "bg-emerald-600 text-white shadow"
                : "text-slate-400 hover:text-white hover:bg-slate-800/60"
            }`}
          >
            <Refrigerator className="h-4 w-4" />
            <span>2. Thực phẩm &amp; Kho tủ lạnh ({inventory.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("optimizer")}
            className={`flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-sm font-semibold transition-colors cursor-pointer ${
              activeTab === "optimizer"
                ? "bg-emerald-600 text-white shadow"
                : "text-slate-400 hover:text-white hover:bg-slate-800/60"
            }`}
          >
            <Calculator className="h-4 w-4" />
            <span>3. Gợi ý Thực đơn Tối ưu</span>
          </button>
        </div>

        {/* Thông báo trạng thái thao tác */}
        {statusMessage && (
          <div
            className={`mb-6 p-3.5 rounded-xl border text-sm flex items-center justify-between ${
              statusMessage.type === "success"
                ? "bg-emerald-950/50 border-emerald-700/60 text-emerald-200"
                : "bg-red-950/50 border-red-700/60 text-red-200"
            }`}
          >
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 shrink-0" />
              <span>{statusMessage.text}</span>
            </div>
            <button
              type="button"
              onClick={() => setStatusMessage(null)}
              className="text-xs underline ml-4 opacity-80 hover:opacity-100 cursor-pointer"
            >
              Đóng
            </button>
          </div>
        )}

        {isLoadingData ? (
          <div className="text-center py-12 text-slate-400">
            Đang tải dữ liệu từ Backend API...
          </div>
        ) : (
          <>
            {/* ============================================================== */}
            {/* MÀN HÌNH 1: TỔNG QUAN & MỤC TIÊU (DASHBOARD & DAILY TARGET)     */}
            {/* ============================================================== */}
            {activeTab === "dashboard" && (
              <div className="space-y-6">
                {/* 4 Thẻ hiển thị Mục tiêu Macro hôm nay */}
                <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
                    <div>
                      <h2 className="text-lg font-bold text-white flex items-center gap-2">
                        <Flame className="h-5 w-5 text-emerald-400" />
                        <span>Mục Tiêu Dinh Dưỡng Hôm Nay</span>
                      </h2>
                      <p className="text-xs text-slate-400">
                        Dữ liệu lấy từ API <code>GET /api/daily-targets/today</code>{" "}
                        &amp; <code>GET /api/dashboard/summary</code>
                      </p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                      Chế độ:{" "}
                      <strong className="text-emerald-400 uppercase">
                        {dashboardSummary?.goalType || "Standard"}
                      </strong>
                    </span>
                  </div>

                  {activeTarget ? (
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                      <div className="p-4 rounded-xl bg-slate-950/80 border border-sky-500/30">
                        <p className="text-xs text-slate-400 uppercase">Tổng Năng Lượng</p>
                        <p className="text-2xl font-extrabold text-sky-400 mt-1">
                          {activeTarget.targetKcal}{" "}
                          <span className="text-xs font-normal text-slate-400">kcal</span>
                        </p>
                      </div>
                      <div className="p-4 rounded-xl bg-slate-950/80 border border-rose-500/30">
                        <p className="text-xs text-slate-400 uppercase">Đạm (Protein)</p>
                        <p className="text-2xl font-extrabold text-rose-400 mt-1">
                          {activeTarget.targetProteinG}{" "}
                          <span className="text-xs font-normal text-slate-400">gram</span>
                        </p>
                      </div>
                      <div className="p-4 rounded-xl bg-slate-950/80 border border-amber-500/30">
                        <p className="text-xs text-slate-400 uppercase">Tinh Bột (Carbs)</p>
                        <p className="text-2xl font-extrabold text-amber-400 mt-1">
                          {activeTarget.targetCarbsG}{" "}
                          <span className="text-xs font-normal text-slate-400">gram</span>
                        </p>
                      </div>
                      <div className="p-4 rounded-xl bg-slate-950/80 border border-emerald-500/30">
                        <p className="text-xs text-slate-400 uppercase">Chất Béo (Fat)</p>
                        <p className="text-2xl font-extrabold text-emerald-400 mt-1">
                          {activeTarget.targetFatG}{" "}
                          <span className="text-xs font-normal text-slate-400">gram</span>
                        </p>
                      </div>
                    </div>
                  ) : (
                    <div className="p-4 rounded-xl bg-amber-950/30 border border-amber-800/50 text-amber-200 text-sm">
                      Hôm nay bạn chưa thiết lập mục tiêu Macro. Hãy nhập ở biểu mẫu bên dưới hoặc bấm nút{" "}
                      <strong>&ldquo;Nạp dữ liệu mẫu (Demo Seed)&rdquo;</strong> trên góc phải!
                    </div>
                  )}
                </div>

                {/* Form thiết lập / cập nhật mục tiêu Macro trong ngày */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <form
                    onSubmit={(e) => void handleSaveDailyTarget(e)}
                    className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4"
                  >
                    <div>
                      <h3 className="text-base font-bold text-white">
                        {todayTarget
                          ? "Cập Nhật Mục Tiêu Macro Hôm Nay (PUT /api/daily-targets)"
                          : "Thiết Lập Mục Tiêu Macro Hôm Nay (POST /api/daily-targets)"}
                      </h3>
                      <p className="text-xs text-slate-400 mt-0.5">
                        Bộ giải OR-Tools sẽ giữ Protein, Carbs, Fat trong biên độ ±5% của mục tiêu này.
                      </p>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-xs font-medium text-slate-300 mb-1">
                          Mục tiêu Calo (kcal)
                        </label>
                        <Input
                          type="number"
                          step="1"
                          min="500"
                          required
                          value={targetKcal}
                          onChange={(e) => setTargetKcal(e.target.value)}
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-medium text-slate-300 mb-1">
                          Mục tiêu Protein (gram)
                        </label>
                        <Input
                          type="number"
                          step="0.5"
                          min="10"
                          required
                          value={targetProteinG}
                          onChange={(e) => setTargetProteinG(e.target.value)}
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-medium text-slate-300 mb-1">
                          Mục tiêu Tinh bột - Carbs (gram)
                        </label>
                        <Input
                          type="number"
                          step="0.5"
                          min="10"
                          required
                          value={targetCarbsG}
                          onChange={(e) => setTargetCarbsG(e.target.value)}
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-medium text-slate-300 mb-1">
                          Mục tiêu Chất béo - Fat (gram)
                        </label>
                        <Input
                          type="number"
                          step="0.5"
                          min="10"
                          required
                          value={targetFatG}
                          onChange={(e) => setTargetFatG(e.target.value)}
                        />
                      </div>
                    </div>

                    <div className="pt-2 flex flex-wrap items-center gap-3">
                      <Button type="submit" disabled={isSavingTarget}>
                        {isSavingTarget
                          ? "Đang lưu..."
                          : todayTarget
                          ? "Cập nhật mục tiêu hôm nay"
                          : "Tạo mục tiêu hôm nay"}
                      </Button>

                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => void handleGenerateOptimalPlan()}
                        disabled={isOptimizing}
                      >
                        Chuyển sang Tính thực đơn tối ưu &rarr;
                      </Button>
                    </div>
                  </form>

                  {/* Thẻ Tóm tắt Kho tủ lạnh hiện tại từ Dashboard Summary */}
                  <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
                    <div>
                      <h3 className="text-base font-bold text-white mb-1">
                        Tóm Tắt Tủ Lạnh Cá Nhân
                      </h3>
                      <p className="text-xs text-slate-400 mb-4">
                        Số nguyên liệu sẵn có để giải bài toán thực đơn
                      </p>

                      <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 mb-4">
                        <p className="text-xs text-slate-400">Tổng số món trong tủ lạnh</p>
                        <p className="text-3xl font-extrabold text-emerald-400 mt-1">
                          {inventory.length}{" "}
                          <span className="text-sm font-normal text-slate-400">
                            nguyên liệu
                          </span>
                        </p>
                      </div>

                      <ul className="space-y-2 text-xs text-slate-300">
                        {inventory.slice(0, 5).map((item) => (
                          <li
                            key={item.inventoryId}
                            className="flex justify-between py-1 border-b border-slate-800/80"
                          >
                            <span>{item.foodName}</span>
                            <span className="font-semibold text-emerald-400">
                              {item.quantityGrams} g
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <Button
                      type="button"
                      variant="secondary"
                      className="w-full mt-4"
                      onClick={() => setActiveTab("inventory")}
                    >
                      Quản lý Kho tủ lạnh &rarr;
                    </Button>
                  </div>
                </div>
              </div>
            )}

            {/* ============================================================== */}
            {/* MÀN HÌNH 2: THỰC PHẨM & KHO TỦ LẠNH (FOODS & INVENTORY)         */}
            {/* ============================================================== */}
            {activeTab === "inventory" && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Form thêm nhanh thực phẩm từ danh sách món ăn (/api/foods) vào tủ lạnh */}
                  <div className="space-y-6">
                    <form
                      onSubmit={(e) => void handleAddInventoryItem(e)}
                      className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-4"
                    >
                      <div className="flex items-center gap-2">
                        <PackagePlus className="h-5 w-5 text-emerald-400" />
                        <h3 className="text-base font-bold text-white">
                          Thêm Thực Phẩm Vào Tủ Lạnh
                        </h3>
                      </div>
                      <p className="text-xs text-slate-400">
                        Chọn món từ <code>GET /api/foods</code> và lưu vào{" "}
                        <code>POST /api/inventory</code>
                      </p>

                      <div>
                        <label className="block text-xs font-medium text-slate-300 mb-1">
                          Chọn món ăn ({foods.length} món có sẵn)
                        </label>
                        <select
                          value={selectedFoodId}
                          onChange={(e) => setSelectedFoodId(e.target.value)}
                          required
                          className="flex h-10 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                        >
                          <option value="" disabled>
                            -- Chọn một thực phẩm --
                          </option>
                          {foods.map((f) => (
                            <option key={f.foodId} value={f.foodId}>
                              {f.categoryName ? `[${f.categoryName}] ` : ""}
                              {f.foodName} ({f.kcalPer100g} kcal | P:{f.proteinGPer100g}g C:
                              {f.carbsGPer100g}g F:{f.fatGPer100g}g /100g)
                            </option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="block text-xs font-medium text-slate-300 mb-1">
                          Số lượng hiện có trong tủ lạnh (gram)
                        </label>
                        <Input
                          type="number"
                          min="1"
                          step="10"
                          required
                          value={quantityGrams}
                          onChange={(e) => setQuantityGrams(e.target.value)}
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-medium text-slate-300 mb-1">
                          Ngày hết hạn (Expiry Date)
                        </label>
                        <Input
                          type="date"
                          value={expiryDate}
                          onChange={(e) => setExpiryDate(e.target.value)}
                        />
                      </div>

                      <Button
                        type="submit"
                        className="w-full"
                        disabled={isAddingInventory || foods.length === 0}
                      >
                        {isAddingInventory ? "Đang thêm..." : "Thêm vào Kho tủ lạnh"}
                      </Button>
                    </form>

                    {/* Form phụ: Tạo món ăn mới vào danh mục hệ thống (/api/foods) */}
                    <form
                      onSubmit={(e) => void handleCreateFood(e)}
                      className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-3"
                    >
                      <div className="flex items-center gap-2">
                        <PlusCircle className="h-4 w-4 text-sky-400" />
                        <h4 className="text-sm font-bold text-white">
                          Thêm Món Mới Vào Danh Mục (/api/foods)
                        </h4>
                      </div>
                      <Input
                        placeholder="Tên món ăn (VD: Cá hồi phi lê)"
                        required
                        value={newFoodName}
                        onChange={(e) => setNewFoodName(e.target.value)}
                      />
                      <div className="grid grid-cols-2 gap-2">
                        <Input
                          type="number"
                          step="0.1"
                          min="0"
                          placeholder="Calo / 100g"
                          required
                          value={newFoodKcal}
                          onChange={(e) => setNewFoodKcal(e.target.value)}
                        />
                        <Input
                          type="number"
                          step="0.1"
                          min="0"
                          placeholder="Protein (g/100g)"
                          required
                          value={newFoodProtein}
                          onChange={(e) => setNewFoodProtein(e.target.value)}
                        />
                        <Input
                          type="number"
                          step="0.1"
                          min="0"
                          placeholder="Carbs (g/100g)"
                          required
                          value={newFoodCarbs}
                          onChange={(e) => setNewFoodCarbs(e.target.value)}
                        />
                        <Input
                          type="number"
                          step="0.1"
                          min="0"
                          placeholder="Fat (g/100g)"
                          required
                          value={newFoodFat}
                          onChange={(e) => setNewFoodFat(e.target.value)}
                        />
                      </div>
                      <Button
                        type="submit"
                        variant="secondary"
                        size="sm"
                        className="w-full"
                        disabled={isCreatingFood}
                      >
                        {isCreatingFood ? "Đang tạo món..." : "Lưu món ăn vào hệ thống"}
                      </Button>
                    </form>
                  </div>

                  {/* Bảng danh sách thực phẩm trong kho cá nhân (/api/inventory) */}
                  <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="text-base font-bold text-white">
                          Danh Sách Nguyên Liệu Trong Kho Tủ Lạnh Cá Nhân
                        </h3>
                        <p className="text-xs text-slate-400">
                          Dữ liệu từ <code>GET /api/inventory</code> (Bản ghi bảng{" "}
                          <code>user_food_inventory</code>)
                        </p>
                      </div>
                      <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                        {inventory.length} món
                      </span>
                    </div>

                    {inventory.length === 0 ? (
                      <div className="text-center py-12 border border-dashed border-slate-800 rounded-xl text-slate-400 text-sm">
                        Kho tủ lạnh của bạn đang trống. Hãy chọn món ăn bên trái để thêm vào kho hoặc bấm nút{" "}
                        <strong className="text-amber-300">
                          &ldquo;Nạp dữ liệu mẫu (Demo Seed)&rdquo;
                        </strong>{" "}
                        trên thanh công cụ!
                      </div>
                    ) : (
                      <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse text-sm">
                          <thead>
                            <tr className="border-b border-slate-800 text-xs uppercase text-slate-400">
                              <th className="py-3 px-3">Tên thực phẩm</th>
                              <th className="py-3 px-3">Tồn kho (gram)</th>
                              <th className="py-3 px-3">Dinh dưỡng / 100g</th>
                              <th className="py-3 px-3">Ngày hết hạn</th>
                              <th className="py-3 px-3 text-right">Thao tác</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-800/70">
                            {inventory.map((item) => (
                              <tr
                                key={item.inventoryId}
                                className="hover:bg-slate-800/40 transition-colors"
                              >
                                <td className="py-3 px-3 font-semibold text-white">
                                  {item.foodName}
                                </td>
                                <td className="py-3 px-3 font-bold text-emerald-400">
                                  {item.quantityGrams} g
                                </td>
                                <td className="py-3 px-3 text-xs text-slate-300">
                                  <span className="text-sky-400 font-medium">
                                    {item.kcalPer100g} kcal
                                  </span>{" "}
                                  | P: {item.proteinGPer100g}g | C: {item.carbsGPer100g}g | F:{" "}
                                  {item.fatGPer100g}g
                                </td>
                                <td className="py-3 px-3 text-xs text-slate-300">
                                  {item.expiryDate || "Không giới hạn"}
                                </td>
                                <td className="py-3 px-3 text-right">
                                  <button
                                    type="button"
                                    onClick={() =>
                                      void handleDeleteInventoryItem(item.inventoryId)
                                    }
                                    className="inline-flex items-center gap-1 text-xs text-red-400 hover:text-red-300 cursor-pointer"
                                    title="Xóa khỏi tủ lạnh"
                                  >
                                    <Trash2 className="h-4 w-4" />
                                    <span>Xóa</span>
                                  </button>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* ============================================================== */}
            {/* MÀN HÌNH 3: GỢI Ý THỰC ĐƠN TỐI ƯU (MEAL OPTIMIZER)             */}
            {/* ============================================================== */}
            {activeTab === "optimizer" && (
              <div className="space-y-6">
                {/* Hộp điều khiển chạy bộ giải OR-Tools */}
                <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div>
                    <h2 className="text-lg font-bold text-white flex items-center gap-2">
                      <Calculator className="h-5 w-5 text-emerald-400" />
                      <span>
                        Bộ Giải Quy Hoạch Tuyến Tính (Google OR-Tools GLOP Solver)
                      </span>
                    </h2>
                    <p className="text-xs text-slate-400 mt-1">
                      Gọi API <code>POST /api/optimizations/generate-plan</code> để tìm số gram
                      thức ăn trong tủ lạnh sao cho đạt Protein, Carbs, Fat (±5%) và độ lệch
                      Calo nhỏ nhất.
                    </p>
                  </div>

                  <Button
                    size="lg"
                    onClick={() => void handleGenerateOptimalPlan()}
                    disabled={isOptimizing}
                    className="shrink-0 gap-2 font-bold shadow-lg shadow-emerald-950/50"
                  >
                    <Calculator className="h-5 w-5" />
                    <span>
                      {isOptimizing
                        ? "Đang giải hệ phương trình..."
                        : "Tính toán khẩu phần ăn tối ưu"}
                    </span>
                  </Button>
                </div>

                {/* Kết quả trả về từ OR-Tools */}
                {optimizationResult ? (
                  <div className="space-y-6">
                    {/* Bảng so sánh Mục tiêu vs. Đạt được */}
                    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
                      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
                        <h3 className="text-base font-bold text-white">
                          1. Đối Chiếu Chỉ Số Dinh Dưỡng (Mục Tiêu vs. Thực Đơn Đạt Được)
                        </h3>
                        <span
                          className={`text-xs font-bold px-3 py-1 rounded-full border ${
                            optimizationResult.solverStatus === "OPTIMAL"
                              ? "bg-emerald-500/15 text-emerald-300 border-emerald-500/40"
                              : optimizationResult.solverStatus === "FEASIBLE"
                              ? "bg-sky-500/15 text-sky-300 border-sky-500/40"
                              : "bg-red-500/15 text-red-300 border-red-500/40"
                          }`}
                        >
                          Trạng thái Solver: {optimizationResult.solverStatus} (Độ lệch Calo:{" "}
                          {optimizationResult.totalDeviationScore} kcal)
                        </span>
                      </div>

                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                          <p className="text-xs text-slate-400">Tổng Calo (kcal)</p>
                          <p className="text-xl font-extrabold text-sky-400 mt-1">
                            {optimizationResult.achievedMacros.kcal}{" "}
                            <span className="text-xs font-normal text-slate-400">
                              / {optimizationResult.targetMacros.kcal} kcal
                            </span>
                          </p>
                        </div>

                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                          <p className="text-xs text-slate-400">Đạm - Protein (±5%)</p>
                          <p className="text-xl font-extrabold text-rose-400 mt-1">
                            {optimizationResult.achievedMacros.proteinG}g{" "}
                            <span className="text-xs font-normal text-slate-400">
                              / {optimizationResult.targetMacros.proteinG}g
                            </span>
                          </p>
                        </div>

                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                          <p className="text-xs text-slate-400">Tinh bột - Carbs (±5%)</p>
                          <p className="text-xl font-extrabold text-amber-400 mt-1">
                            {optimizationResult.achievedMacros.carbsG}g{" "}
                            <span className="text-xs font-normal text-slate-400">
                              / {optimizationResult.targetMacros.carbsG}g
                            </span>
                          </p>
                        </div>

                        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                          <p className="text-xs text-slate-400">Chất béo - Fat (±5%)</p>
                          <p className="text-xl font-extrabold text-emerald-400 mt-1">
                            {optimizationResult.achievedMacros.fatG}g{" "}
                            <span className="text-xs font-normal text-slate-400">
                              / {optimizationResult.targetMacros.fatG}g
                            </span>
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Bảng định lượng chi tiết từng món cần lấy trong kho */}
                    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
                      <h3 className="text-base font-bold text-white mb-1">
                        2. Bảng Khẩu Phần Ăn Tối Ưu Cần Lấy Từ Tủ Lạnh
                      </h3>
                      <p className="text-xs text-slate-400 mb-4">
                        Định lượng chính xác số gram của từng nguyên liệu được giải từ biến quyết
                        định <code>grams[i]</code>
                      </p>

                      {optimizationResult.allocatedItems.length === 0 ? (
                        <div className="p-4 rounded-xl bg-red-950/30 border border-red-800/50 text-red-200 text-sm">
                          Không tìm được tổ hợp món ăn thỏa mãn. Hãy bổ sung thêm thực phẩm vào
                          Kho tủ lạnh hoặc bấm nút{" "}
                          <strong>&ldquo;Nạp dữ liệu mẫu (Demo Seed)&rdquo;</strong>.
                        </div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="w-full text-left border-collapse text-sm">
                            <thead>
                              <tr className="border-b border-slate-800 text-xs uppercase text-slate-400">
                                <th className="py-3 px-3">Món ăn trong kho</th>
                                <th className="py-3 px-3">Khối lượng cần lấy (gram)</th>
                                <th className="py-3 px-3">Calo (kcal)</th>
                                <th className="py-3 px-3">Protein (g)</th>
                                <th className="py-3 px-3">Carbs (g)</th>
                                <th className="py-3 px-3">Fat (g)</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-800/70">
                              {optimizationResult.allocatedItems.map((item) => (
                                <tr
                                  key={item.foodId}
                                  className="hover:bg-slate-800/40 transition-colors"
                                >
                                  <td className="py-3 px-3 font-semibold text-white">
                                    {item.foodName}
                                  </td>
                                  <td className="py-3 px-3 font-extrabold text-emerald-400 text-base">
                                    {item.quantityGrams} g
                                  </td>
                                  <td className="py-3 px-3 text-sky-400 font-medium">
                                    {item.kcal} kcal
                                  </td>
                                  <td className="py-3 px-3 text-rose-400">{item.proteinG} g</td>
                                  <td className="py-3 px-3 text-amber-400">{item.carbsG} g</td>
                                  <td className="py-3 px-3 text-emerald-400">{item.fatG} g</td>
                                </tr>
                              ))}
                            </tbody>
                            <tfoot>
                              <tr className="border-t-2 border-slate-700 font-bold text-white bg-slate-950/60">
                                <td className="py-3 px-3">TỔNG CỘNG ĐẠT ĐƯỢC</td>
                                <td className="py-3 px-3 text-emerald-400">
                                  {optimizationResult.allocatedItems
                                    .reduce((acc, cur) => acc + cur.quantityGrams, 0)
                                    .toFixed(2)}{" "}
                                  g
                                </td>
                                <td className="py-3 px-3 text-sky-400">
                                  {optimizationResult.achievedMacros.kcal} kcal
                                </td>
                                <td className="py-3 px-3 text-rose-400">
                                  {optimizationResult.achievedMacros.proteinG} g
                                </td>
                                <td className="py-3 px-3 text-amber-400">
                                  {optimizationResult.achievedMacros.carbsG} g
                                </td>
                                <td className="py-3 px-3 text-emerald-400">
                                  {optimizationResult.achievedMacros.fatG} g
                                </td>
                              </tr>
                            </tfoot>
                          </table>
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12 bg-slate-900/50 border border-dashed border-slate-800 rounded-2xl text-slate-400 text-sm">
                    Nhấn nút{" "}
                    <strong className="text-emerald-400">
                      &ldquo;Tính toán khẩu phần ăn tối ưu&rdquo;
                    </strong>{" "}
                    ở trên để hệ thống giải bài toán Quy hoạch tuyến tính từ nguyên liệu trong tủ
                    lạnh của bạn.
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
