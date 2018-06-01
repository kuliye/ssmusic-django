function delete_coll(collid){
        if (confirm("确认要删除？")) {
            $.get('/user/coll_delete/?collid='+collid,function (jieguo) {
                if(jieguo.data==1){alert('删除成功');window.location.reload()}
                else{alert('删除失败')}

        })
        }
    }
    function delete_coll_detail(coll_de_id) {
        if (confirm("确认要删除？")) {
            $.get('/user/coll_delete_detail/?colldeid='+coll_de_id,function (jieguo) {
                if(jieguo.data==1){alert('删除成功');window.location.reload()}
                else{alert('删除失败')}
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