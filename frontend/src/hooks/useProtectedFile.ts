import { useEffect, useState } from "react";
import { axiosInstance } from "../utils/axios";

export function useProtectedFile(url: string) {
  const [src, setSrc] = useState<string | null>(null);

  useEffect(() => {
    if (!url) return;

    let objectUrl: string | null = null;

    axiosInstance
      .get(url, { responseType: "blob" })
      .then(res => {
        objectUrl = URL.createObjectURL(res.data);
        setSrc(objectUrl);
      })
      .catch(err => console.error("Error while loading file:", err));

    return () => {
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [url]);

  return src;
}
