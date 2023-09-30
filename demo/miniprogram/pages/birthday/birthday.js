const db =wx.cloud.database();
Page({

  /**
   * 页面的初始数据
   */
  data: {
        user:{name:'' ,birthday:''}
      },

    getbirthday(event) {
          console.log('获取输入的生日', event.detail.value)
          this.setData({
            birthday: event.detail.value
          })
        },

      change() {
        let birthday = this.data.birthday
        let userCollection = db.collection('user')
        var name2=wx.getStorageSync('_name')
        userCollection.where({
            name: name2
        })
          .update({
            data: {
              birthday: birthday
            }
          })
          .then(res => {
            console.log('更新成功')
            wx.showToast({
                icon: '',
                title: '更新成功',
              })
            this.setData({
              birthday: birthday,
            })

          })
      },
      back:function(){
            console.log('Back')
            wx.reLaunch({
              url: '/pages/personal/personal',
            })
          },

})