"use client";
import { Controller, useFormContext } from "react-hook-form";
import { mainFormData } from "../types/main-form-data";
import { Button, DatePicker, Input } from "@heroui/react";

interface Props {
  onSubmit: () => void;
}

const MainForm = ({ onSubmit }: Props) => {
  const { handleSubmit, register, control } = useFormContext<mainFormData>();

  return (
    <div className="">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col space-y-4 p-4"
      >
        <div>
          <h3 className="text-xl font-medium">Enter the following details</h3>
          <p className="text-default-500">
            We will use this to give a prediction model of your business
          </p>
        </div>
        <div className="flex space-x-2">
          <Input
            type="text"
            label="Restaurant Name"
            {...register("restaurantName", { required: true })}
          />
          <Input
            type="text"
            label="Cuisine"
            {...register("cuisine", { required: true })}
          />
        </div>
        <div className="flex space-x-2">
          <Input
            type="text"
            label="Location"
            {...register("location", { required: true })}
          />
          <Input
            type="text"
            label="City"
            {...register("city", { required: true })}
          />
        </div>

        <div className="flex space-x-2">
          <Input
            type="number"
            label="Sales Amount"
            {...register("salesAmount", {
              required: true,
              valueAsNumber: true,
              min: 0,
            })}
          />
          <Input
            type="number"
            label="Sales Quantity"
            {...register("salesQuantity", {
              required: true,
              valueAsNumber: true,
              min: 0,
            })}
          />
          <Controller
            name="date"
            control={control}
            rules={{ required: true }}
            render={({ field }) => (
              <DatePicker label="Date of establishment" {...field} />
            )}
          />
          <Input
            type="number"
            label="Rating"
            {...register("rating", {
              required: true,
              valueAsNumber: true,
              min: 0,
              max: 5,
            })}
          />
        </div>
        <Button className="mt-3 w-10" size="lg" type="submit" color="primary">
          Submit
        </Button>
      </form>
    </div>
  );
};

export default MainForm;
