-- CreateTable
CREATE TABLE "RadarEvent" (
    "id" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "startTime" TIMESTAMP(3) NOT NULL,
    "description" TEXT,

    CONSTRAINT "RadarEvent_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Forecast" (
    "id" TEXT NOT NULL,
    "eventId" TEXT NOT NULL,
    "modelVersion" TEXT NOT NULL,
    "latencyMs" INTEGER NOT NULL,
    "csiConvlstm" JSONB NOT NULL,
    "csiPersist" JSONB NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Forecast_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "RadarEvent_slug_key" ON "RadarEvent"("slug");

-- CreateIndex
CREATE INDEX "Forecast_eventId_createdAt_idx" ON "Forecast"("eventId", "createdAt");

-- AddForeignKey
ALTER TABLE "Forecast" ADD CONSTRAINT "Forecast_eventId_fkey" FOREIGN KEY ("eventId") REFERENCES "RadarEvent"("id") ON DELETE CASCADE ON UPDATE CASCADE;
