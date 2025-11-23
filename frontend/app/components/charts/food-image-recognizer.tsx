import { Button, Card, CardBody } from "@heroui/react";
import { ArrowUpRightIcon } from "lucide-react";
import Link from "next/link";
import React from "react";

const FoodImageRecognizer = () => {
  return (
    <Card className="col-span-6">
      <CardBody className="flex flex-row items-center space-x-3">
        <p className="text-2xl text-secondary-700">
          Try our food image recognizer!
        </p>
        <Link
          className="ml-auto"
          href={
            "https://huggingface.co/spaces/DonyiCoder2006/Food_Image_Recogniser"
          }
        >
          <Button
            color="secondary"
            size="lg"
            variant="bordered"
            endContent={<ArrowUpRightIcon size={30} />}
          >
            Food Image Recognizer
          </Button>
        </Link>
      </CardBody>
    </Card>
  );
};

export default FoodImageRecognizer;
