import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import HomepageFeatures from "@site/src/components/HomepageFeatures";

import styles from "./index.module.css";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg margin-right--md"
            to="/docs/intro"
          >
            Installation
          </Link>
          <Link
            className="button button--secondary button--lg margin-right--md"
            to="/docs/common-patterns"
          >
            Common Patterns
          </Link>
          <Link
            className="button button--secondary button--lg margin-right--md"
            to="/docs/category/sdk-reference"
          >
            SDK Reference
          </Link>
        </div>
      </div>
    </header>
  );
}
// Installation
// <p>Install the SDK and get your credentials in the right place</p>
// <Link to="/docs/intro">See installation guide 👉</Link>

const HomepageCard = ({
  title,
  link,
  children,
}: {
  title: string;
  link?: JSX.Element;
  children: JSX.Element;
}): JSX.Element => {
  return (
    <div className="card shadow--lw">
      <div className="card__header">
        <h3>{title}</h3>
      </div>
      <div className="card__body">{children}</div>
      <div className="card__footer" style={{ textAlign: "right" }}>
        {link}
      </div>
    </div>
  );
};

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout title={`Home`} description="Aurora Origin SDK Docs">
      <HomepageHeader />
      <main>
        <div className="container margin-top--md">
          <p>
            This documentation should hopefully get you up and running with the
            SDK. Please be aware the project is under active development.
          </p>
          <h2>Topics</h2>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "2rem",
            }}
          >
            <HomepageCard
              title="Installation"
              link={<Link to="/docs/intro">See installation guide 👉</Link>}
            >
              <p>Install the SDK and get your credentials in the right place</p>
            </HomepageCard>

            <HomepageCard
              title="Common Patterns"
              link={
                <Link to="/docs/common-patterns">See what's possible ✨</Link>
              }
            >
              <p>
                Some useful patterns that can get you started quickly, or serve
                as inspiration for the things you might want to do.
              </p>
            </HomepageCard>

            <HomepageCard
              title="Reference Guide"
              link={
                <Link to="/docs/category/sdk-reference">
                  Get into the details 👨‍🔬
                </Link>
              }
            >
              <p>
                All exported and documented interfaces. Not beginner friendly,
                but the most complete form of documentation we offer.
              </p>
            </HomepageCard>
          </div>
        </div>
      </main>
    </Layout>
  );
}
