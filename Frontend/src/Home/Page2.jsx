import React from "react";
import QueueAnim from "rc-queue-anim";
import OverPack from "rc-scroll-anim/lib/ScrollOverPack";

export default function Page2() {
  return (
    <OverPack component="section" className="page-wrapper page2">
      <QueueAnim
        type="bottom"
        className="page text-center"
        leaveReverse
        key="page"
      >
        <h2 key="title">GI-IADS Platform</h2>
        <span key="line" className="separator" />
        <QueueAnim type="bottom" className="info-content" key="content">
          <p className="main-info" key="1">
            GI-IADS stands at the forefront of no-code machine learning,
            offering a platform that seamlessly transforms data into actionable
            insights. From predictive analytics to image recognition, its
            versatile capabilities empower users to effortlessly build, deploy,
            and manage machine learning models. With an intuitive interface,
            GI-IADS ensures that both beginners and seasoned professionals can
            unlock the power of machine learning, fostering innovation and
            informed decision-making across a spectrum of applications.
          </p>
        </QueueAnim>
      </QueueAnim>
    </OverPack>
  );
}
