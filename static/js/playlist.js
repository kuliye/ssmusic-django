var aud=$('#audio')
    aud.onended=function () {
        alert('播放结束')
    }
    function delete_playlist(musicid) {
        if (confirm("确认要删除？")) {
            $.get('/playlist_delete/?musicid='+musicid,function (jieguo) {
                if(jieguo.data==1){
                    window.location.reload()
                }else{
                    alert('删除失败')
                }
            })
        }
    }
    function play(musicid) {
        $.get('/playmusic/?musicid='+musicid,function (jieguo) {

                $('#src').html('<audio autoplay controls id="audio"> <source src='+jieguo.src+ ' type="audio/mpeg"> </audio>')

        })
    }