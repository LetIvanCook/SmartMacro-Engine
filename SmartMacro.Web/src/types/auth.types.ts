export interface RegisterRequestDto {
  email: string;
  password: string;
  fullName: string;
  dateOfBirth: string; // YYYY-MM-DD
  biologicalSex: string; // "male" | "female"
  activityLevel?: string; // "sedentary" | "light" | "moderate" | "heavy" | "athlete"
  goalType?: string; // "cutting" | "bulking" | "maintenance"
}

export interface LoginRequestDto {
  email: string;
  password: string;
}

export interface AuthResponseDto {
  accessToken: string;
  refreshToken: string;
  accessTokenExpiry: string;
  userId: number;
  email: string;
  fullName?: string | null;
}

export interface RefreshTokenRequestDto {
  refreshToken: string;
}

export interface UserSession {
  userId: number;
  email: string;
  fullName?: string | null;
}

