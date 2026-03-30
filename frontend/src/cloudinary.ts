import { Cloudinary } from "@cloudinary/url-gen";
import { thumbnail } from "@cloudinary/url-gen/actions/resize";
import { FocusOn } from "@cloudinary/url-gen/qualifiers/focusOn";
import { focusOn } from "@cloudinary/url-gen/qualifiers/gravity";
import axios from "axios";

const CLOUD_NAME = import.meta.env.VITE_CLOUDINARY_NAME;

export const CLD_URL = `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/image/upload`;

export const cld = new Cloudinary({
  cloud: {
    cloudName: CLOUD_NAME,
    apiKey: import.meta.env.VITE_CLOUDINARY_API_KEY,
    apiSecret: import.meta.env.VITE_CLOUDINARY_API_SECRET,
  },
});

export function getAvatar(publicId: string, width: number = 40, height: number = 40) {
  return cld.image(publicId).resize(
    thumbnail().width(width).height(height).gravity(focusOn(FocusOn.face())),
  ).format("auto").quality("auto");
}

export async function uploadToCloudinary(file: File): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("upload_preset", "ml_default");
  formData.append("api_key", import.meta.env.VITE_CLOUDINARY_API_KEY);
  const response = await axios.post(CLD_URL, formData);
  return response.data.public_id;
}

export async function deleteFromCloudinary(imageUrl: string): Promise<string> {
  const response = await axios.delete(`${CLD_URL}/${imageUrl}`);
  return response.data.public_id;
}
