# ── Stage 1: Build & Publish ─────────────────────────────────────
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies
COPY ["SmartMacro.Api/SmartMacro.Api.csproj", "SmartMacro.Api/"]
RUN dotnet restore "SmartMacro.Api/SmartMacro.Api.csproj"

# Copy full source and publish
COPY . .
WORKDIR "/src/SmartMacro.Api"
RUN dotnet publish "SmartMacro.Api.csproj" -c Release -o /app/publish /p:UseAppHost=false

# ── Stage 2: Runtime Image ────────────────────────────────────────
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

EXPOSE 8080

ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:8080

COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "SmartMacro.Api.dll"]
