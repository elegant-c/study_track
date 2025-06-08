const path = require('path');
const vue = require('@vitejs/plugin-vue');

module.exports = {
  plugins: [vue()],
  resolve: {
    alias: [
      {
        find: "@",
        replacement: path.resolve(__dirname, './src')
      },
    ]
  },
};
