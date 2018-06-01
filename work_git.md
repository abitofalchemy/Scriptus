# Notes for working with Git

From [link][1]
> git checkout master
    git pull
    git checkout mobiledevicesupport
    git merge master
    to keep mobiledevicesupport in sync with master

then when you're ready to put mobiledevicesupport into master, first merge in master like above, then ...

>   git checkout master
    git merge mobiledevicesupport
    git push origin master


References

[1]:https://stackoverflow.com/questions/16329776/how-to-keep-a-git-branch-in-sync-with-master

