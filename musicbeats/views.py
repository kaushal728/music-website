from django.shortcuts import render
from .models import Channel, Song, Watchlater, History
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.shortcuts import redirect
from django.db.models import Case, When
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user, music_id=music_id)
        history.save()

        return redirect(f"/musicbeats/songs/{music_id}")

    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, 'musicbeats/history.htm', {"history": song})



def watchlater(request):
    
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        watch = Watchlater.objects.filter(user=user)

        for i in watch:
            if video_id == i.video_id:
                message = "Your Video is Already Added"
                break
        else:
            watchlater = Watchlater(user=user, video_id=video_id)
            watchlater.save()
            message = "Your Video is Succesfully Added"

        song = Song.objects.filter(song_id=video_id).first()
        return render(request, f"musicbeats/songpost.htm", {'song': song, "message": message})

    wl = Watchlater.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "musicbeats/watchlater.htm", {'song': song})




def songs(request):
    song = Song.objects.all()
    return render(request, 'musicbeats/songs.htm', {'song':song})



def playlist(request):
    cid = '024d0f3645aa4f7a947b16108d83696d'
    secret = 'c85eba690e174939a78f08fc1794bced'
    artist_uri = 'https://open.spotify.com/artist/4YRxDV8wJFPHPTeXepOstw?si=YxEzi7cTSPGc6cSGx1xgOA'

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(cid, secret))
    song = spotify.artist_top_tracks(artist_uri)

    song_details = []

    for track in song['tracks']:
        title = track['name']
        song_url = track['preview_url']
        images = track['album']['images'][0]['url']
        singer = track['artists'][0]['name']
        song_id = track['id']
        song_details.append([title, song_url, images, singer, song_id])
        # print(song_details)

    return render(request, 'musicbeats/playlist.htm', {'song':song_details})



def secondplaylist(request):
    cid = '024d0f3645aa4f7a947b16108d83696d'
    secret = 'c85eba690e174939a78f08fc1794bced'
    artist_uri2 = 'https://open.spotify.com/artist/7vk5e3vY1uw9plTHJAMwjN?si=nfXVmtZ6ROqCT0u-RyROjQ'

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(cid, secret))
    song2 = spotify.artist_top_tracks(artist_uri2)

    song_details2 = []

    for track in song2['tracks']:
        title2 = track['name']
        song_url2 = track['preview_url']
        images2 = track['album']['images'][0]['url']
        singer2 = track['artists'][0]['name']
        song_id2 = track['id']
        song_details2.append([title2, song_url2, images2, singer2, song_id2])

    return render(request, 'musicbeats/secondplaylist.htm', {'second':song_details2})


def thirdplaylist(request):
    cid = '024d0f3645aa4f7a947b16108d83696d'
    secret = 'c85eba690e174939a78f08fc1794bced'
    artist_url = 'https://open.spotify.com/artist/7uIbLdzzSEqnX0Pkrb56cR?si=VTnrCNYyT6yGgy2NwwQz1A'
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(cid, secret))
    song2 = spotify.artist_top_tracks(artist_url)

    song_details = []

    for track in song2['tracks']:
        title2 = track['name']
        song_url2 = track['preview_url']
        images2 = track['album']['images'][0]['url']
        singer2 = track['artists'][0]['name']
        song_id2 = track['id']
        print(song_url2)
        song_details.append([title2, song_url2, images2, singer2, song_id2])

    return render(request, 'musicbeats/thirdplaylist.htm', {'third':song_details})



def songpost(request, id):
    song = Song.objects.filter(song_id=id).first()
    allsong = Song.objects.all()
    
    return render(request, 'musicbeats/songpost.htm', {'song': song, 'allsong':allsong})




def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        from django.contrib.auth import login
        login(request, user)   
        return redirect('/')

    return render(request, 'musicbeats/login.htm')




def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        user = authenticate(username=username, password=pass1)
        from django.contrib.auth import login
        login(request, user)

        channel = Channel(name=username)
        channel.save()

        return redirect('/')

    return render(request, 'musicbeats/signup.htm')




def logout_user(request):
    logout(request)
    return redirect("/")




def channel(request, channel):
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    song = Song.objects.filter(song_id__in=video_ids).order_by(preserved)    

    return render(request, "musicbeats/channel.htm", {"channel": chan, "song": song})




def upload(request):
    if request.method == "POST":
        name = request.POST['name']
        singer = request.POST['singer']
        tag = request.POST['tag']
        image = request.FILES['image']
        movie = request.POST['movie']
        song1 = request.FILES['file']

        song_model = Song(name=name, singer=singer, tags=tag, image=image, movie=movie, song=song1)
        song_model.save()

        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name=str(request.user))
        print(channel_find)

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()

    return render(request, "musicbeats/upload.htm")




def search(request):
    query = request.GET.get("query")
    song = Song.objects.all()
    qs = song.filter(name__icontains=query)

    return render(request, "musicbeats/search.htm", {"songs":qs, "query":query})

