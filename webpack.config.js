module.exports = {
  entry: {
    main: "./frontend/SomePage.js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
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
