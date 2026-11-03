// Các kiểu dữ liệu (DTO) khớp trực tiếp với Backend ASP.NET Core 8

export interface DailyTargetResponseDto {
  id: number;
  targetDate: string; // YYYY-MM-DD
  targetKcal: number;
  targetProteinG: number;
  targetCarbsG: number;
  targetFatG: number;
}

export interface CreateDailyTargetRequestDto {
  date?: string | null;
  targetKcal: number;
  targetProteinG: number;
  targetCarbsG: number;
  targetFatG: number;
}

export interface UpdateDailyTargetRequestDto {
  targetKcal: number;
  targetProteinG: number;
  targetCarbsG: number;
  targetFatG: number;
}

export interface FoodResponseDto {
  foodId: number;
  foodName: string;
  categoryId?: number | null;
  categoryName?: string | null;
  kcalPer100g: number;
  proteinGPer100g: number;
  carbsGPer100g: number;
  fatGPer100g: number;
  fiberGPer100g?: number | null;
  isVerified: boolean;
  source: string;
  createdAt: string;
}

export interface PagedResult<T> {
  items: T[];
  totalCount: number;
  page: number;
  pageSize: number;
}

export interface CreateFoodRequestDto {
  foodName: string;
  categoryId?: number | null;
  kcalPer100g: number;
  proteinGPer100g: number;
  carbsGPer100g: number;
  fatGPer100g: number;
  fiberGPer100g?: number | null;
}

export interface InventoryItemResponseDto {
  inventoryId: number;
  foodId: number;
  foodName: string;
  quantityGrams: number;
  expiryDate?: string | null; // YYYY-MM-DD
  kcalPer100g: number;
  proteinGPer100g: number;
  carbsGPer100g: number;
  fatGPer100g: number;
}

export interface CreateInventoryItemRequestDto {
  foodId: number;
  quantityGrams: number;
  expiryDate?: string | null;
}

export interface DailyTargetSummaryDto {
  targetKcal: number;
  targetProteinG: number;
  targetCarbsG: number;
  targetFatG: number;
}

export interface UserDashboardResponseDto {
  userId: number;
  fullName?: string | null;
  goalType: string;
  todayTarget?: DailyTargetSummaryDto | null;
  availableInventory: InventoryItemResponseDto[];
}

export interface OptimizationRequestDto {
  dailyTargetId?: number | null;
  includeFoodIds?: number[] | null;
}

export interface MacroSummaryDto {
  kcal: number;
  proteinG: number;
  carbsG: number;
  fatG: number;
}

export interface AllocatedFoodItemDto {
  foodId: number;
  foodName: string;
  quantityGrams: number;
  kcal: number;
  proteinG: number;
  carbsG: number;
  fatG: number;
}

export interface OptimizationResultDto {
  solverStatus: string; // "OPTIMAL" | "FEASIBLE" | "INFEASIBLE"
  totalDeviationScore: number;
  targetMacros: MacroSummaryDto;
  achievedMacros: MacroSummaryDto;
  allocatedItems: AllocatedFoodItemDto[];
}
