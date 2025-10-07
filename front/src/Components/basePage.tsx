import AREA from "../../favicon.svg";
import home from "@material-design-icons/svg/round/home.svg";
import folder from "@material-design-icons/svg/round/folder.svg";
import density_medium from "@material-design-icons/svg/round/density_medium.svg";
import keyboard_arrow_down from "@material-design-icons/svg/round/keyboard_arrow_down.svg";
import "./style.scss";
import type { PropsWithChildren, ReactNode } from "react";

type BasePageProps = PropsWithChildren<{
  title?: string; // page title (last breadcrumb)
  pageTitle?: string[]; // breadcrumb parts shown in center
  userInitial?: string; // initial shown in user-icon
}>;

export default function BasePage({
  children,
  title = "MyWorkflow",
  pageTitle = ["Page title", "/", "goes here"],
  userInitial = "L",
}: BasePageProps) {
  const titleNodes: ReactNode[] = [];
  pageTitle.forEach((b, i) => {
    if (i > 0)
      titleNodes.push(
        <div key={`sep-${i}`} className="text-wrapper">
          /
        </div>
      );
    titleNodes.push(
      <div key={`b-${i}`} className="text-wrapper">
        {b}
      </div>
    );
  });
  // append title as final breadcrumb if provided and different from last breadcrumb
  if (
    title &&
    (pageTitle.length === 0 || pageTitle[pageTitle.length - 1] !== title)
  ) {
    titleNodes.push(
      <div key={`sep-title`} className="text-wrapper">
        /
      </div>
    );
    titleNodes.push(
      <div key={`title`} className="text-wrapper">
        {title}
      </div>
    );
  }

  return (
    <div className="base-page">
      <div className="top-bar">
        <div className="top-left-corner">
          <button className="vector-button" aria-label="Home">
            <img className="img" alt="Home" src={home} />
          </button>
        </div>

        <div className="top-content">
          <div className="left">
            <div className="text-wrapper">-</div>

            <div className="app-title">
              <div className="vector-wrapper">
                <img className="img" alt="Area" src={AREA} />
              </div>

              <div className="text-wrapper">Area</div>
            </div>
          </div>

          <div className="center">
            <div className="vector-wrapper">
              <img className="img" alt="Folder" src={folder} />
            </div>

            {titleNodes}

            <div className="vector-wrapper">
              <img
                className="img"
                alt="Keyboard Arrow Down"
                src={keyboard_arrow_down}
              />
            </div>
          </div>

          <div className="right">
            <div className="user-icon">
              <div className="div">{userInitial}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="center-content">
        <div className="left-bar">
          <div className="vector-wrapper">
            <img className="img" alt="Density Medium" src={density_medium} />
          </div>
        </div>

        <div className="main-content">{children}</div>
      </div>
    </div>
  );
}
