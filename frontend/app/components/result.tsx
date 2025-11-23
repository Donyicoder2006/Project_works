"use client";

import { useFormContext } from "react-hook-form";
import { mainFormData } from "../types/main-form-data";
import CityChart from "./charts/city-chart";
import FeedbackChart from "./charts/feedback-chart";
import MonthChart from "./charts/month-chart";
import RatingChart from "./charts/rating-chart";
import SuccessChart from "./charts/success-chart";
import UserDetails from "./charts/user-details";
import useSWR from "swr";
import { unifiedApi } from "../types/api-types";
import { Card, CardBody, CircularProgress } from "@heroui/react";
import Insight from "./charts/insight";
import { CircleXIcon } from "lucide-react";
import FoodImageRecognizer from "./charts/food-image-recognizer";

const fetcher = ([url, payload]: [url: string, payload: mainFormData]) =>
  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      year: payload.date.year,
      month: payload.date.month,
      sales_qty: payload.salesQuantity,
      sales_amount: payload.salesAmount,
      Ratings: payload.rating,
      Resturant_Name: payload.restaurantName,
      City: payload.city,
      Cuisine: payload.cuisine,
      Location: payload.location,
    }),
  }).then((r) => r.json());

const Result = () => {
  const { getValues } = useFormContext<mainFormData>();
  const payload = getValues();
  const { data, error, isLoading } = useSWR<unifiedApi>(
    [`${process.env.NEXT_PUBLIC_API_URL}/predict/unified`, payload],
    fetcher
  );

  if (isLoading)
    return (
      <div className="w-full p-3 flex items-center space-x-5">
        <CircularProgress size="md" />
        <p className="text-default-400 dark:text-default-400 text-2xl">
          Hold on... we're spicing up your predictions!
        </p>
      </div>
    );
  if (!data)
    return (
      <Card>
        <CardBody className="justify-center items-center py-5 space-y-2">
          <CircleXIcon color="var(--color-red-400)" size={80} />
          <p className="text-3xl text-red-300">Could not load models!</p>
          <p className="text-lg text-red-300">
            Please ensure you have access to the models API
          </p>
        </CardBody>
      </Card>
    );

  return (
    <div className="grid grid-cols-6 gap-2 grid-flow-dense">
      <UserDetails />
      <FeedbackChart data={data} />
      <SuccessChart data={data} />
      <RatingChart data={data} />
      <CityChart data={data} />
      <MonthChart data={data} />
      <Insight data={data} />
      <FoodImageRecognizer />
    </div>
  );
};

export default Result;
