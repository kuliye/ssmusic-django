function add_playlist(musicid){
        $.get('/add_music/?music_id='+musicid,function (jieguo) {
            if(jieguo.data==1){
                alert('已添加至播放列表')
            }else{
                alert('添加失败')
            }
        })
    }