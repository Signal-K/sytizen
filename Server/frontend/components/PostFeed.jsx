import Link from "next/link";

export default function PostFeed({ posts }) {
    return (
      <div className="p-2">
        {posts
          ? posts.map((post) => <PostItem post={post} key={post.id} />)
          : null}
      </div>
    );
}

function PostItem({ post }) {
    let imageURL;
    if (post.metadata.image) { // IPFS gateway (URI/url)
        imageURL = post.metadata.image.replace("ipfs://", 'https://ipfs.io/ipfs'); // Replace ipfs link with a regular http ref.uri
    }

    return (
        <div>
            <Link href={`/posts/${post.id}`}>
                <img src={imageURL} />
                <h2>{post.metadata.name}</h2>
            </Link>
        </div>
    )
}