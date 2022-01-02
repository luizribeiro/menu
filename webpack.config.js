module.exports = {
  entry: {
    main: "./frontend/SomePage.tsx",
  },
  module: {
    rules: [
      {
        test: /\.(js|ts)x?$/,
        use: "babel-loader",
      },
      {
        test: /\.(svg|png|jpg|jpeg|gif)$/,
        loader: "file-loader",

        options: {
          name: "[name].[ext]",
          outputPath: "./dist",
        },
      },
    ],
  },
  output: {
    path: __dirname + "/dist",
    filename: "[name].bundle.js",
  },
};
