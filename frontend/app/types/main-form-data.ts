import { CalendarDate } from "@internationalized/date";

export type mainFormData = {
  city: string;
  cuisine: string;
  date: CalendarDate;
  salesQuantity: number;
  salesAmount: number;
  rating: number;
  restaurantName: string;
};
