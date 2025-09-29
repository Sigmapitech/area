{
  stdenv,
  gradle,
  jdk,
  front,
  nodejs
}:

stdenv.mkDerivation (finalAttrs: {
  pname = "area-mobile-apk";
  version = "0.0.1";

  src = ./.;

  buildInputs = [
    jdk
    nodejs
  ];

 nativeBuildInputs = [
    gradle
  ];

  gradleFlags = [
    "-Pjdk_home=${jdk}"
  ];

  mitmCache = gradle.fetchDeps {
    pkg = finalAttrs.finalPackage;

    data = ./deps.json;
  };

  preBuild = ''
    # cp -r ${front} dist
    npx cap sync android
  '';

  installPhase = ''
    runHook preInstall

    # Copy the APK(s) to $out
    mkdir -p $out
    cp -v android/app/build/outputs/apk/release/*.apk $out/

    runHook postInstall
  '';
})
