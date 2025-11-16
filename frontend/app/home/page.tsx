"use client";

import { Card, CardBody, Tab, Tabs } from "@heroui/react";
import React from "react";
import { useForm } from "react-hook-form";
import { mainFormData } from "../types/main-form-data";
import MainForm from "../components/main-form";

const HomePage = () => {
  const form = useForm<mainFormData>();

  return (
    <div className="p-3 flex flex-col space-y-4">
      <h2 className="text-primary-600 text-2xl font-semibold">Welcome!</h2>
      <Tabs aria-label="Steps">
        <Tab key="form" title="Form">
          <Card>
            <CardBody>
              <MainForm form={form} />
            </CardBody>
          </Card>
        </Tab>
        <Tab key="music" title="Result" isDisabled={true}>
          <Card>
            <CardBody>Work in progress</CardBody>
          </Card>
        </Tab>
      </Tabs>
    </div>
  );
};

export default HomePage;
