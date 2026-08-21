import { create } from "zustand";
import type { AuthResponseDto, UserSession } from "../types/auth.types";

interface AuthState {
  accessToken: string | null;
  user: UserSession | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setAuth: (data: AuthResponseDto) => void;
  setAccessToken: (token: string) => void;
  logout: () => void;
  getRefreshToken: () => string | null;
}

const REFRESH_TOKEN_KEY = "smartmacro_refresh_token";
const USER_KEY = "smartmacro_user";

export const useAuthStore = create<AuthState>((set) => {
  // Try restoring cached user info from storage for seamless initial render
  const savedUser = localStorage.getItem(USER_KEY);
  const parsedUser = savedUser ? (JSON.parse(savedUser) as UserSession) : null;
  const hasRefreshToken = !!localStorage.getItem(REFRESH_TOKEN_KEY);

  return {
    accessToken: null,
    user: parsedUser,
    isAuthenticated: hasRefreshToken,
    isLoading: false,

    setAuth: (data: AuthResponseDto) => {
      localStorage.setItem(REFRESH_TOKEN_KEY, data.refreshToken);
      const user: UserSession = {
        userId: data.userId,
        email: data.email,
        fullName: data.fullName,
      };
      localStorage.setItem(USER_KEY, JSON.stringify(user));

      set({
        accessToken: data.accessToken,
        user,
        isAuthenticated: true,
        isLoading: false,
      });
    },

    setAccessToken: (token: string) => {
      set({ accessToken: token, isAuthenticated: true });
    },

    logout: () => {
      localStorage.removeItem(REFRESH_TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      set({
        accessToken: null,
        user: null,
        isAuthenticated: false,
        isLoading: false,
      });
    },

    getRefreshToken: () => {
      return localStorage.getItem(REFRESH_TOKEN_KEY);
    },
  };
});

