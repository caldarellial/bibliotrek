import { useEffect, useMemo, useState } from "react";
import { View, Image, Square } from "tamagui";

export const IntroScreen = () => {
  const [startIntro, setStartIntro] = useState(false);

  const imgSrc = useMemo(
    () =>
      startIntro
        ? require("../../../../assets/images/bag-opened.jpg")
        : require("../../../../assets/splash-icon.png"),
    [startIntro],
  );

  useEffect(() => {
    setTimeout(() => {
      setStartIntro(true);
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
