export default function PostFeed({ posts }) { // Take posts as an input parameter & return mapping of all posts items from Constants/context
    return (
        <div className="p-2">
            {posts
                ? posts.map((post) => <PostItem post={post} key={post.id} />)
                : null}
        </div>
    )
}

function PostItem({ post }) {
    let imageURL;
    if (post.metadata.image) { // IPFS gateway (URI/url)
        imageURL = post.metadata.image.replace("ipfs://", 'https://ipfs.io/ipfs'); // Replace ipfs link with a regular http ref.uri
    }

    return (
        <div>
            <img src={imageURL} />
            <h2>{post.metadata.name}</h2>
        </div>
    )
}