import { apiClient } from "./client";
import type {
  CreateDailyTargetRequestDto,
  CreateFoodRequestDto,
  CreateInventoryItemRequestDto,
  DailyTargetResponseDto,
  FoodResponseDto,
  InventoryItemResponseDto,
  OptimizationRequestDto,
  OptimizationResultDto,
  PagedResult,
  UpdateDailyTargetRequestDto,
  UserDashboardResponseDto,
} from "../types/macro.types";

export const macroApi = {
  // 1. Màn hình 1: Tổng quan & Mục tiêu hôm nay
  getDashboardSummary: async (): Promise<UserDashboardResponseDto> => {
    const response = await apiClient.get<UserDashboardResponseDto>("/dashboard/summary");
    return response.data;
  },

  getTodayTarget: async (): Promise<DailyTargetResponseDto | null> => {
    try {
      const response = await apiClient.get<DailyTargetResponseDto>("/daily-targets/today");
      return response.data;
    } catch {
      // Nếu hôm nay chưa thiết lập mục tiêu (HTTP 404), trả về null
      return null;
    }
  },

  createDailyTarget: async (
    payload: CreateDailyTargetRequestDto
  ): Promise<DailyTargetResponseDto> => {
    const response = await apiClient.post<DailyTargetResponseDto>("/daily-targets", payload);
    return response.data;
  },

  updateDailyTarget: async (
    id: number,
    payload: UpdateDailyTargetRequestDto
  ): Promise<DailyTargetResponseDto> => {
    const response = await apiClient.put<DailyTargetResponseDto>(
      `/daily-targets/${id}`,
      payload
    );
    return response.data;
  },

  // 2. Màn hình 2: Danh mục món ăn & Kho tủ lạnh cá nhân
  getFoods: async (keyword = "", pageSize = 50): Promise<PagedResult<FoodResponseDto>> => {
    const response = await apiClient.get<PagedResult<FoodResponseDto>>("/foods", {
      params: { keyword: keyword || undefined, page: 1, pageSize },
    });
    return response.data;
  },

  createFood: async (payload: CreateFoodRequestDto): Promise<FoodResponseDto> => {
    const response = await apiClient.post<FoodResponseDto>("/foods", payload);
    return response.data;
  },

  getInventory: async (): Promise<InventoryItemResponseDto[]> => {
    const response = await apiClient.get<InventoryItemResponseDto[]>("/inventory");
    return response.data;
  },

  addInventoryItem: async (
    payload: CreateInventoryItemRequestDto
  ): Promise<InventoryItemResponseDto> => {
    const response = await apiClient.post<InventoryItemResponseDto>("/inventory", payload);
    return response.data;
  },

  deleteInventoryItem: async (itemId: number): Promise<void> => {
    await apiClient.delete(`/inventory/${itemId}`);
  },

  // 3. Màn hình 3: Gợi ý thực đơn tối ưu (Google OR-Tools GLOP Solver)
  generateMealPlan: async (
    payload: OptimizationRequestDto = {}
  ): Promise<OptimizationResultDto> => {
    const response = await apiClient.post<OptimizationResultDto>(
      "/optimizations/generate-plan",
      payload
    );
    return response.data;
  },
};
