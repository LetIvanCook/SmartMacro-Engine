import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Link } from "react-router-dom";
import { Lock, Mail, User, Calendar, Dumbbell, Loader2, AlertCircle } from "lucide-react";
import { useAuth } from "../hooks/useAuth";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "../components/ui/card";
import axios from "axios";

const registerSchema = z.object({
  fullName: z.string().min(2, "Họ tên phải từ 2 ký tự trở lên"),
  email: z.string().min(1, "Email không được để trống").email("Email không hợp lệ"),
  password: z.string().min(6, "Mật khẩu tối thiểu 6 ký tự"),
  dateOfBirth: z.string().min(1, "Vui lòng chọn ngày sinh"),
  biologicalSex: z.enum(["male", "female"], {
    message: "Vui lòng chọn giới tính sinh học",
  }),
  activityLevel: z.enum(["sedentary", "light", "moderate", "heavy", "athlete"]),
  goalType: z.enum(["cutting", "bulking", "maintenance"]),
});

type RegisterFormValues = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const { register: registerAccount, isRegistering } = useAuth();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      fullName: "",
      email: "",
      password: "",
      dateOfBirth: "2000-01-01",
      biologicalSex: "male",
      activityLevel: "moderate",
      goalType: "maintenance",
    },
  });

  const onSubmit = async (values: RegisterFormValues) => {
    setErrorMessage(null);
    try {
      await registerAccount(values);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        if (err.response?.status === 409) {
          setErrorMessage("Email này đã được đăng ký trong hệ thống. Vui lòng sử dụng email khác.");
        } else {
          setErrorMessage(err.response?.data?.detail || "Đăng ký không thành công. Vui lòng kiểm tra lại thông tin.");
        }
      } else {
        setErrorMessage("Lỗi kết nối máy chủ. Vui lòng kiểm tra kết nối mạng.");
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <div className="w-full max-w-lg">
        {/* Branding */}
        <div className="flex flex-col items-center mb-6">
          <div className="h-14 w-14 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-950/50 mb-2 border border-emerald-400/30">
            <Dumbbell className="h-8 w-8 text-slate-950 stroke-[2.5]" />
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-white">
            Tạo Tài Khoản <span className="text-emerald-400">SmartMacro</span>
          </h1>
          <p className="text-slate-400 text-xs text-center mt-1">
            Bắt đầu hành trình kiểm soát dinh dưỡng chính xác từng gram
          </p>
        </div>

        {/* Register Card */}
        <Card className="border-slate-800/80 shadow-2xl">
          <CardHeader className="space-y-1 pb-3">
            <CardTitle className="text-lg font-semibold text-slate-100">Thông Tin Cá Nhân</CardTitle>
            <CardDescription>Nhập thông tin ban đầu để tính toán BMR & Macro</CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-3.5">
              {errorMessage && (
                <div className="p-3 rounded-lg bg-red-950/50 border border-red-800/50 flex items-start gap-2 text-xs text-red-200">
                  <AlertCircle className="h-4 w-4 text-red-400 shrink-0 mt-0.5" />
                  <span>{errorMessage}</span>
                </div>
              )}

              {/* Full Name */}
              <div className="space-y-1">
                <Label htmlFor="fullName">Họ và tên</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                  <Input
                    id="fullName"
                    placeholder="Nguyễn Văn A"
                    className="pl-9"
                    {...register("fullName")}
                    disabled={isRegistering}
                  />
                </div>
                {errors.fullName && (
                  <p className="text-xs text-red-400">{errors.fullName.message}</p>
                )}
              </div>

              {/* Email */}
              <div className="space-y-1">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="nguyenvana@gmail.com"
                    className="pl-9"
                    {...register("email")}
                    disabled={isRegistering}
                  />
                </div>
                {errors.email && (
                  <p className="text-xs text-red-400">{errors.email.message}</p>
                )}
              </div>

              {/* Password */}
              <div className="space-y-1">
                <Label htmlFor="password">Mật khẩu</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="Tối thiểu 6 ký tự"
                    className="pl-9"
                    {...register("password")}
                    disabled={isRegistering}
                  />
                </div>
                {errors.password && (
                  <p className="text-xs text-red-400">{errors.password.message}</p>
                )}
              </div>

              {/* Date of Birth & Sex */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="space-y-1">
                  <Label htmlFor="dateOfBirth">Ngày sinh</Label>
                  <div className="relative">
                    <Calendar className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                    <Input
                      id="dateOfBirth"
                      type="date"
                      className="pl-9"
                      {...register("dateOfBirth")}
                      disabled={isRegistering}
                    />
                  </div>
                  {errors.dateOfBirth && (
                    <p className="text-xs text-red-400">{errors.dateOfBirth.message}</p>
                  )}
                </div>

                <div className="space-y-1">
                  <Label htmlFor="biologicalSex">Giới tính sinh học</Label>
                  <select
                    id="biologicalSex"
                    className="flex h-10 w-full rounded-lg border border-slate-700 bg-slate-900/80 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    {...register("biologicalSex")}
                    disabled={isRegistering}
                  >
                    <option value="male">Nam (Male)</option>
                    <option value="female">Nữ (Female)</option>
                  </select>
                  {errors.biologicalSex && (
                    <p className="text-xs text-red-400">{errors.biologicalSex.message}</p>
                  )}
                </div>
              </div>

              {/* Activity & Goal */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="space-y-1">
                  <Label htmlFor="activityLevel">Mức độ vận động</Label>
                  <select
                    id="activityLevel"
                    className="flex h-10 w-full rounded-lg border border-slate-700 bg-slate-900/80 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    {...register("activityLevel")}
                    disabled={isRegistering}
                  >
                    <option value="sedentary">Ít vận động (Văn phòng)</option>
                    <option value="light">Vận động nhẹ (1-3 ngày/tuần)</option>
                    <option value="moderate">Vừa phải (3-5 ngày/tuần)</option>
                    <option value="heavy">Nhiều (6-7 ngày/tuần)</option>
                    <option value="athlete">Vận động viên</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <Label htmlFor="goalType">Mục tiêu hiện tại</Label>
                  <select
                    id="goalType"
                    className="flex h-10 w-full rounded-lg border border-slate-700 bg-slate-900/80 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    {...register("goalType")}
                    disabled={isRegistering}
                  >
                    <option value="cutting">Giảm mỡ (Cutting / Fat Loss)</option>
                    <option value="maintenance">Giữ cân (Maintenance)</option>
                    <option value="bulking">Tăng cơ (Bulking / Muscle Gain)</option>
                  </select>
                </div>
              </div>

              <Button
                type="submit"
                className="w-full mt-3 font-semibold"
                size="lg"
                disabled={isRegistering}
              >
                {isRegistering ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Đang tạo tài khoản...
                  </>
                ) : (
                  "Hoàn Tất Đăng Ký"
                )}
              </Button>
            </form>
          </CardContent>

          <CardFooter className="flex justify-center border-t border-slate-800/80 pt-3 text-sm text-slate-400">
            Đã có tài khoản?{" "}
            <Link
              to="/login"
              className="ml-1.5 font-medium text-emerald-400 hover:text-emerald-300 transition-colors"
            >
              Đăng nhập
            </Link>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

