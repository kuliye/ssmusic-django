function delete_album(albumid){
        if (confirm("确认要删除？")) {
            $.get('/user/delete_album/?albumid='+albumid,function (jieguo) {
                if(jieguo.data==1){
                alert('删除成功');window.location.reload()}
                else{
                    alert('删除失败')
                }
            })
    }}
    function delete_album_detail(musicid) {
        if (confirm("确认要删除？")) {
            $.get('/user/delete_album_detail/?musicid='+musicid,function (jieguo) {
                if(jieguo.data==1){
                alert('删除成功');window.location.reload()}
                else{
                    alert('删除失败')
                }
            })
        }
    }
    function add_playlist(musicid){
        $.get('/add_music/?music_id='+musicid,function (jieguo) {
            if(jieguo.data==1){
                alert('已添加至播放列表')
            }else{
                alert('添加失败')
            }
        })
    }