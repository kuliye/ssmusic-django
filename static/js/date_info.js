 function fun(event) {
      $.get('/add_music/?music_id='+event,function() {
          alert('添加成功')

            })
     }
     function bofang(musicid) {
         $.get('/playmusic/?musicid='+musicid,function (jieguo) {
             $("#src").html('<audio autoplay controls id="audio"> <source src='+jieguo.src+ ' type="audio/mpeg"> </audio>')
         })

     }
     function coll_add(musicid,collid) {
        $.get('/coll_handle/?musicid='+musicid+'&collection='+collid,function (jieguo) {
            if(jieguo.data==1){
                alert('添加成功')
            }else if (jieguo.data==2){
                alert('该收藏夹已经存在此音乐')
            }else{
                alert('未知原因收藏失败')
            }
        })
     }

