const db =wx.cloud.database();
Page({

  /**
   * 页面的初始数据
   */
  data: {
        user:{name:'' , password:'',number:''}
      },

    getnumber(event) {
          console.log('获取输入的手机号', event.detail.value)
          this.setData({
            number: event.detail.value
          })
        },

      change() {
        let number = this.data.number
        let userCollection = db.collection('user')
        userCollection.where({
            name: wx.getStorageSync('_name')
        })
          .update({
            data: {
              number: number
            }
          })
          .then(res => {
            console.log('更新成功')
            wx.showToast({
                icon: '',
                title: '更新成功',
              })
            this.setData({
              number: number,
            })
          })
      },
      onShow() {
        wx.hideHomeButton();
        wx.hideShareMenu();
      },
      back:function(){
            console.log('Back')
            wx.reLaunch({
              url: '/pages/personal/personal',
            })
          },
        login(event){
          wx.navigateBack({
              delta:1
          })
      }

})