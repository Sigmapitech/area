interface SubmitOptions<T> {
  url: string;
  method?: "POST" | "GET" | "PUT" | "DELETE";
  body: T;
  onSuccess: (data: any) => void;
  onError?: (error: any) => void;
}

function handleSubmitError(error: any): string {
  if (Array.isArray(error.detail)) {
    return error.detail.map((e: any) => e.msg || JSON.stringify(e)).join(", ");
  }

  if (typeof error.detail === "string") {
    return error.detail;
  }

  return "An unexpected error occurred";
}

export async function handleFormSubmit<T>({
  url,
  method = "POST",
  body,
  onSuccess,
  onError,
}: SubmitOptions<T>) {
  try {
    const response = await fetch(url, {
      method,
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json();
      onError?.(handleSubmitError(error));
    } else {
      const data = await response.json();
      onSuccess(data);
    }
  } catch (err: any) {
    onError?.(err.detail || err.message || "error");
  }
}
