"use client";

import { Card, CardBody, Tab, Tabs } from "@heroui/react";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { mainFormData } from "../types/main-form-data";
import MainForm from "../components/main-form";
import Result from "../components/result";
import { parseDate } from "@internationalized/date";
import ThemeToggle from "../components/theme-toggle";
import { BrainCogIcon, GithubIcon } from "lucide-react";
import Link from "next/link";
import { useTheme } from "next-themes";

const HomePage = () => {
  const methods = useForm<mainFormData>({});
  const [tabState, setTabState] = useState<string>("form");
  const { resolvedTheme, setTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  const {
    formState: { isSubmitted },
  } = methods;

  const onSubmit = () => {
    setTabState("result");
  };

  return (
    <div className="p-3 flex flex-col space-y-4">
      <div className="fixed -z-1 top-0 left-0 rounded-none w-full">
        {/* <div className="z-0 w-screen h-screen opacity-45 backdrop-opacity-35 bg-linear-to-r from-red-500 via-amber-500 to-orange-500"></div> */}
        <img
          className="-z-1 w-screen h-screen rounded-none opacity-60 dark:opacity-20
          "
          width={"100%"}
          height={"100%"}
          src={
            "https://img.freepik.com/premium-photo/raw-salmon-fillet-ingredients-cooking-dark-background-rustic-style-top-view_80295-2052.jpg?w=2000"
          }
        />
      </div>
      <nav className="sticky top-5 z-10">
        <Card>
          <CardBody className="flex flex-row items-center space-x-3">
            <BrainCogIcon size={36} color="var(--color-orange-400)" />
            <h2 className="text-2xl font-semibold text-orange-600">
              Restaurant Success Predictor
            </h2>
            <span className="ml-auto"></span>
            <Link href={"https://github.com/Donyicoder2006/Project_works"}>
              <button
                className={`p-1 transition-colors duration-200 rounded-md
                  text-default-600 hover:text-default-900 cursor-pointer`}
              >
                <GithubIcon />
              </button>
            </Link>
            <ThemeToggle />
          </CardBody>
        </Card>
      </nav>
      <div className="absolute top-4 right-4"></div>
      <FormProvider {...methods}>
        <Tabs
          aria-label="Steps"
          selectedKey={tabState}
          onSelectionChange={(e) => setTabState(String(e))}
        >
          <Tab key="form" title="Form">
            <Card>
              <CardBody>
                <MainForm onSubmit={onSubmit} />
              </CardBody>
            </Card>
          </Tab>
          <Tab key="result" title="Result" isDisabled={!isSubmitted}>
            <Card>
              <CardBody>
                <Result />
              </CardBody>
            </Card>
          </Tab>
        </Tabs>
      </FormProvider>
    </div>
  );
};

export default HomePage;
