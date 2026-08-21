# ── Stage 1: Build & Publish ─────────────────────────────────────
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies for layer caching
COPY ["SmartMacro.Api/SmartMacro.Api.csproj", "SmartMacro.Api/"]
RUN dotnet restore "SmartMacro.Api/SmartMacro.Api.csproj"

# Copy full source and publish
COPY . .
WORKDIR "/src/SmartMacro.Api"
RUN dotnet publish "SmartMacro.Api.csproj" -c Release -o /app/publish --no-restore /p:UseAppHost=false

# ── Stage 2: Runtime Image (Hardened, Minimal, Non-Root, glibc-compatible) ──
FROM mcr.microsoft.com/dotnet/aspnet:8.0-bookworm-slim AS runtime
WORKDIR /app

# Install wget for healthcheck and clean apt caches to keep image minimal
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user and group, create logs and dp-keys directories with proper ownership
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser && \
    mkdir -p /app/logs /app/dp-keys && chown -R appuser:appgroup /app

# Security note: perl-base and ncurses-base/ncurses-bin are Essential packages
# in Debian bookworm-slim. Purging Essential packages risks breaking the system
# package manager during subsequent build layers and is not safe to force.
# Neither library has any code path called by this application or the .NET runtime.
# All related CVEs have no HTTP attack vector in this deployment model.
# Risk accepted — documented in GitHub Issues #6, #7, #8 and Trivy scan report.

# Copy published application from build stage
COPY --from=build --chown=appuser:appgroup /app/publish .

EXPOSE 8080

ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:8080

# Switch to non-root user
USER appuser

# Container healthcheck using wget on liveness endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["dotnet", "SmartMacro.Api.dll"]
