"use client";
import { feedbackApi, healthApi } from "@/app/types/api-types";
import { mainFormData } from "@/app/types/main-form-data";
import { capitalize } from "@/app/utils/text";
import { Card, CardBody } from "@heroui/react";
import { StarIcon } from "lucide-react";
import { useFormContext } from "react-hook-form";
import useSWR from "swr";

enum Colors {
  Green = "#a3e635",
  Yellow = "#facc15",
  Orange = "#fb923c",
}

enum FeedBackStates {
  Poor = "poor feedback",
  Medium = "median feedback",
  Excellent = "excellent feedback",
}

const fetcher = ([url, payload]: [url: string, payload: mainFormData]) =>
  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      Resturant_Name: payload.restaurantName,
      Cuisine: payload.cuisine,
      Location: payload.location,
      City: payload.city,
    }),
  }).then((r) => r.json());

const FeedbackChart = () => {
  const { getValues } = useFormContext<mainFormData>();
  const payload = getValues();
  const { data, error, isLoading } = useSWR<feedbackApi>(
    [`${process.env.NEXT_PUBLIC_API_URL}/predict/feedback`, payload],
    fetcher
  );

  if (!data) return <div>Not found</div>;

  const feedbackState = data.feedback_prediction;

  const selectedColor =
    feedbackState === FeedBackStates.Excellent
      ? Colors.Green
      : feedbackState === FeedBackStates.Medium
      ? Colors.Yellow
      : feedbackState === FeedBackStates.Poor
      ? Colors.Orange
      : "black";

  return (
    <Card>
      <CardBody className="flex items-center justify-center">
        <h3 className="self-start">Rating Prediction</h3>
        <div className="flex space-x-2">
          <StarIcon color={selectedColor} fill={selectedColor} size={60} />
          <StarIcon
            color={
              [FeedBackStates.Excellent, FeedBackStates.Medium].includes(
                feedbackState as FeedBackStates
              )
                ? selectedColor
                : "darkgrey"
            }
            fill={
              [FeedBackStates.Excellent, FeedBackStates.Medium].includes(
                feedbackState as FeedBackStates
              )
                ? selectedColor
                : "darkgrey"
            }
            size={60}
          />
          <StarIcon
            color={
              feedbackState === FeedBackStates.Excellent
                ? selectedColor
                : "darkgrey"
            }
            fill={
              feedbackState === FeedBackStates.Excellent
                ? selectedColor
                : "darkgrey"
            }
            size={60}
          />
        </div>
        <p className={`text-2xl`} style={{ color: selectedColor }}>
          {capitalize(feedbackState)}
        </p>
      </CardBody>
    </Card>
  );
};

export default FeedbackChart;
