const db = wx.cloud.database();
Page({

  data: {
    user: {
      name: '',
      password: ''
    }
  },

  getname(event) {
    console.log('获取输入的用户名', event.detail.value)
    this.setData({
      name: event.detail.value
    })
  },

  password(event) {
    console.log('获取输入的密码', event.detail.value)
    this.setData({
      password: event.detail.value
    })
  },

  getpassword(event) {
    console.log('获取输入的新密码', event.detail.value)
    this.setData({
      newpassword: event.detail.value
    })
  },

  confirm(event) {
    console.log('确认的密码', event.detail.value)
    this.setData({
      confirm: event.detail.value
    })
  },


  change() {
    let name = this.data.name
    let password = this.data.password
    let newpassword = this.data.newpassword
    let confirm = this.data.confirm
    let userCollection = db.collection('user')
    userCollection.where({})
      .get().then(res => {
        console.log(res.data)
        if (res.data[0].password != password) {
          wx.showToast({
            icon: 'none',
            title: '密码错误',
          })
          return
        } else if (newpassword.length < 2 || newpassword.length > 10) {
          wx.showToast({
            icon: 'none',
            title: '密码长度应大于2小于10',
          })
          return
        } else if (newpassword != confirm) {
          wx.showToast({
            icon: 'none',
            title: '密码不一致',
          })
          return
        } else {
          userCollection.where({
              name: wx.getStorageSync('_name')
            })
            .update({
              data: {
                password: newpassword
              }
            })
            .then(res => {
              console.log('更新成功')
              wx.showToast({
                icon: '',
                title: '更新成功',
              })
              this.setData({
                password: newpassword,
              })
            }).catch(err => {
              console.log('更新失败', err) //失败提示错误信息
            })
        }
      })
  },






  back: function () {
    console.log('Back')
    wx.reLaunch({
      url: '/pages/home/home',
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
