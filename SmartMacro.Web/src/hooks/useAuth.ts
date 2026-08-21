import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { authApi } from "../api/auth.api";
import { useAuthStore } from "../stores/auth.store";
import type { LoginRequestDto, RegisterRequestDto } from "../types/auth.types";

export function useAuth() {
  const navigate = useNavigate();
  const { setAuth, logout: clearAuthStore, isAuthenticated, user, getRefreshToken } =
    useAuthStore();

  const loginMutation = useMutation({
    mutationFn: (credentials: LoginRequestDto) => authApi.login(credentials),
    onSuccess: (data) => {
      setAuth(data);
      navigate("/dashboard", { replace: true });
    },
  });

  const registerMutation = useMutation({
    mutationFn: (payload: RegisterRequestDto) => authApi.register(payload),
    onSuccess: (data) => {
      setAuth(data);
      navigate("/dashboard", { replace: true });
    },
  });

  const logoutMutation = useMutation({
    mutationFn: async () => {
      const refreshToken = getRefreshToken();
      if (refreshToken) {
        try {
          await authApi.logout(refreshToken);
        } catch {
          // Ignore server logout errors on client logout
        }
      }
    },
    onSettled: () => {
      clearAuthStore();
      navigate("/login", { replace: true });
    },
  });

  return {
    login: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    loginError: loginMutation.error,

    register: registerMutation.mutateAsync,
    isRegistering: registerMutation.isPending,
    registerError: registerMutation.error,

    logout: logoutMutation.mutateAsync,
    isLoggingOut: logoutMutation.isPending,

    isAuthenticated,
    user,
  };
}

