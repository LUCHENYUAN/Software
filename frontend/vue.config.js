// vue.config.js for less-loader@6.0.0
module.exports = {
    css: {
      loaderOptions: {
        less: {
          lessOptions: {
            modifyVars: {
              'primary-color': '#517E55',
              'link-color': '#517E55',
              'btn-border-radius-sm': '0px',
            },
            javascriptEnabled: true,
          },
        },
      },
    },
    configureWebpack: {},
    devServer: { // 环境配置
      host: '0.0.0.0',
      public: 'http://127.0.0.1', // 此处是自己电脑IP地址！
      port: '8080',
      // proxy: 'http://localhost:5000/',
      https: false,
      disableHostCheck: true,
      open: false // 配置自动启动浏览器
    }
  };