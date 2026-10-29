import React from "react";
import { Composition } from "remotion";
import { ExplainerVideo } from "./ExplainerVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ExplainerVideo"
      component={ExplainerVideo}
      durationInFrames={7200} // 240 seconds at 30 fps
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{
        storyboardPath: "../../storyboard/storyboard.json",
      }}
    />
  );
};
