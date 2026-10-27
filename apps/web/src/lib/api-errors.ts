import { NextResponse } from "next/server";

export function errorResponse(status: number, code: string, message: string): NextResponse {
  return NextResponse.json({ error: { code, message } }, { status });
}

export function databaseUnavailableResponse(): NextResponse {
  console.error("[api] database unavailable");
  return errorResponse(503, "database_unavailable", "Database unavailable");
}
