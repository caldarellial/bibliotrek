import { useEffect, useMemo, useState } from "react";
import * as SplashScreen from "expo-splash-screen";
import { View, Image, Square } from "tamagui";

SplashScreen.preventAutoHideAsync();

export const IntroScreen = ({ onComplete }: { onComplete: () => void }) => {
  const [startIntro, setStartIntro] = useState(false);

  const imgSrc = useMemo(
    () =>
      startIntro
        ? require("../../../../assets/images/bag-opened.png")
        : require("../../../../assets/splash-icon.png"),
    [startIntro],
  );

  useEffect(() => {
    setTimeout(() => {
      setStartIntro(true);
      SplashScreen.hideAsync();

      setTimeout(() => {
        onComplete();
      }, 2000);
    }, 1000);
  }, []);

  return (
    <View
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100%"
      width="100%"
      backgroundColor="#22415E"
    >
      <Square
        backgroundColor="white"
        transition={"lazy"}
        size={1000}
        circular
        position="absolute"
        scale={startIntro ? 1 : 0.01}
      />
      <Image src={imgSrc} width={200} height={200} />
    </View>
  );
};
