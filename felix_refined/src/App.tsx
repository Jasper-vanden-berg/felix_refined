import { GitHubBanner, Refine } from "@refinedev/core";
import { DevtoolsPanel, DevtoolsProvider } from "@refinedev/devtools";
import { RefineKbar, RefineKbarProvider } from "@refinedev/kbar";

import {
  ErrorComponent,
  ThemedLayout,
  ThemedSider,
  useNotificationProvider,
} from "@refinedev/antd";
import "@refinedev/antd/dist/reset.css";

import routerProvider, {
  DocumentTitleHandler,
  NavigateToResource,
  UnsavedChangesNotifier,
} from "@refinedev/react-router";
import { App as AntdApp } from "antd";
import { BrowserRouter, Outlet, Route, Routes } from "react-router";
import { Header } from "./components/header";
import { ColorModeContextProvider } from "./contexts/color-mode";

import {
  CategoryCreate,
  CategoryEdit,
  CategoryList,
  CategoryShow,
} from "./pages/categories";
import { dataProvider } from "./providers/data";

import { Autopsies } from "./pages/autopsies";
import { FreezerList } from "./pages/freezers";
import { Genomics } from "./pages/genomics";
import { Inventory } from "./pages/inventory";
import { Options } from "./pages/options";
import { Summaries } from "./pages/summaries";

function App() {
  return (
    <BrowserRouter>
      <RefineKbarProvider>
        <ColorModeContextProvider>
          <AntdApp>
            <DevtoolsProvider>
              <Refine
                dataProvider={dataProvider}
                notificationProvider={useNotificationProvider}
                routerProvider={routerProvider}
                resources={[
                  {
                    name: "Autopsies",
                    list: "/autopsies",
                  },
                  {
                    name: "Freezers",
                    list: "/freezers",
                  },
                  {
                    name: "Inventory",
                    list: "/inventory",
                  },
                  {
                    name: "Summaries",
                    list: "/summaries",
                  },
                  {
                    name: "Genomics",
                    list: "/genomics",
                  },
                  {
                    name: "Options",
                    list: "/options",
                  },
                  {
                    name: "categories",
                    list: "/categories",
                    create: "/categories/create",
                    edit: "/categories/edit/:id",
                    show: "/categories/show/:id",
                    meta: {
                      canDelete: true,
                    },
                  },
                ]}
                options={{
                  syncWithLocation: true,
                  warnWhenUnsavedChanges: true,
                }}
              >
                <Routes>
                  <Route
                    element={
                      <ThemedLayout
                        Header={() => <Header sticky />}
                        Sider={(props) => <ThemedSider {...props} fixed />}
                      >
                        <Outlet />
                      </ThemedLayout>
                    }
                  >
                    <Route
                      index
                      element={<NavigateToResource resource="blog_posts" />}
                    />
                    <Route path="/autopsies">
                      <Route index element={<Autopsies />} />
                    </Route>

                    <Route path="/freezers">
                      <Route index element={<FreezerList />} />
                    </Route>

                    <Route path="/inventory">
                      <Route index element={<Inventory />} />
                    </Route>

                    <Route path="/summaries">
                      <Route index element={<Summaries />} />
                    </Route>
                    
                    <Route path="/genomics">
                      <Route index element={<Genomics />} />
                    </Route>
                    
                    <Route path="/options">
                      <Route index element={<Options />} />
                    </Route>
                    <Route path="/categories">
                      <Route index element={<CategoryList />} />
                      <Route path="create" element={<CategoryCreate />} />
                      <Route path="edit/:id" element={<CategoryEdit />} />
                      <Route path="show/:id" element={<CategoryShow />} />
                    </Route>
                    <Route path="*" element={<ErrorComponent />} />
                  </Route>
                </Routes>

                <RefineKbar />
                <UnsavedChangesNotifier />
                <DocumentTitleHandler />
              </Refine>
              <DevtoolsPanel />
            </DevtoolsProvider>
          </AntdApp>
        </ColorModeContextProvider>
      </RefineKbarProvider>
    </BrowserRouter>
  );
}

export default App;
