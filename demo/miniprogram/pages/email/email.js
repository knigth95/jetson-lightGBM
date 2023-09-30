const db =wx.cloud.database();
Page({

  /**
   * 页面的初始数据
   */
  data: {
        user:{name:'' ,emali:''}
      },

    getemail(event) {
          console.log('获取输入的邮箱', event.detail.value)
          this.setData({
            email: event.detail.value
          })
        },

      change() {
        let email = this.data.email
        let userCollection = db.collection('user')
        userCollection.where({
            name: wx.getStorageSync('_name')
        })
          .update({
            data: {
              email: email
            }
          })
          .then(res => {
            console.log('更新成功')
            wx.showToast({
                icon: '',
                title: '更新成功',
              })
            this.setData({
             email : email,
            })
          })
      },
      back:function(){
            console.log('Back')
            wx.reLaunch({
              url: '/pages/personal/personal',
            })
          },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})