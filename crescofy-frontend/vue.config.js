module.exports = {
    publicPath: './',
    configureWebpack: {
        devtool: 'source-map',
        devServer: {
            watchOptions: {
                ignored: [/node_modules/, /public/],
            }
        }
    }
}
