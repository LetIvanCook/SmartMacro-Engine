import { apiClient } from "./client";
import type {
  AuthResponseDto,
  LoginRequestDto,
  RegisterRequestDto,
  RefreshTokenRequestDto,
} from "../types/auth.types";

export const authApi = {
  login: async (credentials: LoginRequestDto): Promise<AuthResponseDto> => {
    const response = await apiClient.post<AuthResponseDto>(
      "/auth/login",
      credentials
    );
    return response.data;
  },

  register: async (payload: RegisterRequestDto): Promise<AuthResponseDto> => {
    const response = await apiClient.post<AuthResponseDto>(
      "/auth/register",
      payload
    );
    return response.data;
  },

  refreshToken: async (
    payload: RefreshTokenRequestDto
  ): Promise<AuthResponseDto> => {
    const response = await apiClient.post<AuthResponseDto>(
      "/auth/refresh",
      payload
    );
    return response.data;
  },

  logout: async (refreshToken: string): Promise<{ message: string }> => {
    const response = await apiClient.post<{ message: string }>("/auth/logout", {
      refreshToken,
    });
    return response.data;
  },
};

