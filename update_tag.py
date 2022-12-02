import os


TAGS_FILE = "tags.txt"
POSTS_FOLDER = "posts"
TAG_SEPARATOR = ","
TAG_POST_SEPERATOR = ":"

tags = dict()
for filename in os.listdir(POSTS_FOLDER):
    with open(os.path.join(POSTS_FOLDER, filename)) as f:
        f.readline()
        for t in f.readline().split(TAG_SEPARATOR):
            t = t.strip()
            if len(t) > 30:
                raise ValueError("Tags must not be longer than 30 characters!")
            tags[t] = tags.get(t, []) + [filename]

with open(TAGS_FILE, "w") as f:
    f.writelines(
        [
            t.strip() + TAG_POST_SEPERATOR + TAG_SEPARATOR.join(posts) + os.linesep
            for t, posts in tags.items()
        ]
    )
