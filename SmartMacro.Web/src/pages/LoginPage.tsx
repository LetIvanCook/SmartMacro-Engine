import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Link } from "react-router-dom";
import { Lock, Mail, Dumbbell, Loader2, AlertCircle } from "lucide-react";
import { useAuth } from "../hooks/useAuth";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "../components/ui/card";
import axios from "axios";

const loginSchema = z.object({
  email: z.string().min(1, "Email không được để trống").email("Email không hợp lệ"),
  password: z.string().min(6, "Mật khẩu tối thiểu 6 ký tự"),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const { login, isLoggingIn } = useAuth();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (values: LoginFormValues) => {
    setErrorMessage(null);
    try {
      await login(values);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        if (err.response?.status === 401) {
          setErrorMessage("Email hoặc mật khẩu không chính xác.");
        } else if (err.response?.status === 429) {
          setErrorMessage("Bạn đã gửi quá nhiều yêu cầu đăng nhập. Vui lòng thử lại sau 1 phút.");
        } else {
          setErrorMessage(err.response?.data?.detail || "Đã xảy ra lỗi đăng nhập. Vui lòng thử lại.");
        }
      } else {
        setErrorMessage("Lỗi kết nối máy chủ. Vui lòng kiểm tra mạng.");
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <div className="w-full max-w-md">
        {/* App Branding */}
        <div className="flex flex-col items-center mb-8">
          <div className="h-16 w-16 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-950/50 mb-3 border border-emerald-400/30">
            <Dumbbell className="h-9 w-9 text-slate-950 stroke-[2.5]" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white mb-1">
            SmartMacro <span className="text-emerald-400">Engine</span>
          </h1>
          <p className="text-slate-400 text-sm text-center">
            Hệ thống tối ưu dinh dưỡng & khẩu phần chuẩn Macro
          </p>
        </div>

        {/* Login Card */}
        <Card className="border-slate-800/80 shadow-2xl">
          <CardHeader className="space-y-1 pb-4">
            <CardTitle className="text-xl font-semibold text-slate-100">Đăng Nhập</CardTitle>
            <CardDescription>Nhập thông tin tài khoản để truy cập dashboard</CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              {errorMessage && (
                <div className="p-3 rounded-lg bg-red-950/50 border border-red-800/50 flex items-start gap-2.5 text-sm text-red-200">
                  <AlertCircle className="h-4 w-4 text-red-400 mt-0.5 shrink-0" />
                  <span>{errorMessage}</span>
                </div>
              )}

              {/* Email */}
              <div className="space-y-1.5">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="user@smartmacro.vn"
                    className="pl-9"
                    {...register("email")}
                    disabled={isLoggingIn}
                  />
                </div>
                {errors.email && (
                  <p className="text-xs text-red-400">{errors.email.message}</p>
                )}
              </div>

              {/* Password */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password">Mật khẩu</Label>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    className="pl-9"
                    {...register("password")}
                    disabled={isLoggingIn}
                  />
                </div>
                {errors.password && (
                  <p className="text-xs text-red-400">{errors.password.message}</p>
                )}
              </div>

              <Button
                type="submit"
                className="w-full mt-2 font-semibold"
                size="lg"
                disabled={isLoggingIn}
              >
                {isLoggingIn ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Đang xác thực...
                  </>
                ) : (
                  "Đăng Nhập"
                )}
              </Button>
            </form>
          </CardContent>

          <CardFooter className="flex justify-center border-t border-slate-800/80 pt-4 text-sm text-slate-400">
            Chưa có tài khoản?{" "}
            <Link
              to="/register"
              className="ml-1.5 font-medium text-emerald-400 hover:text-emerald-300 transition-colors"
            >
              Đăng ký ngay
            </Link>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

