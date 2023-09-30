const db =wx.cloud.database();
Page({
    data: {
        name:''
    },
        
    onLoad:function(options){
        const name = wx.getStorageSync('name')
        this.setData({
            name: name
        });
        console.log('欢迎'+this.data.name)
        db.collection('user').where({
            name:this.data.name
        })
        .get().then(res =>{
            if(res.data[0].number==undefined){
                wx.showModal({
                    content: '为了方便找回信息，请在个人资料界面完善个人信息',
                    showCancel:false,
                    confirmText:"我知道了",
                    cancelColor: '#666666',//666666
                    confirmColor: '#666666',
                  })
            }
        })
    },

    navigateToSleepHealth(event){
        console.log('查看睡眠健康')
        wx.navigateTo({
          url: '/pages/sleepheath/sleepheath',
        })
    },

      tolog(){
        wx.navigateTo({
            url: '/pages/sleeplog/slleeplog',
          })
      },

    navigateToSleepLog(event){
        console.log('查看睡眠日志')
        wx.navigateTo({
          url: '/pages/sleeptime/sleeptime',
        })
    },

    navigateToSleepHeartRate(event){
        console.log('查看睡眠心率')
        wx.navigateTo({
          url: '/pages/sleeprate/sleeprate',
        })
    },

    logout: function () {
        wx.showModal({
          content: '确定退出登录吗？',
          cancelColor: '#666666',//666666
          confirmColor: '#666666',
          success(res) {
            if (res.confirm) {
              wx.reLaunch({
                url: '/pages/login/login',
              })
              console.log('用户点击确定')
            } else if (res.cancel) {
              console.log('用户点击取消')
            }
          },
          fail: function (res) { },//接口调用失败的回调函数
          complete: function (res) { },//接口调用结束的回调函数（调用成功、失败都会执行
        })
     
      },

      //修改密码
  updatepassword:function () {
    wx.navigateTo({
      url: '/pages/updatepassword/updatepassword',
    })
  },

  //个人资料界面跳转
  bind:function(){
    wx.navigateTo({
      url: '/pages/personal/personal',
    })
  },
})