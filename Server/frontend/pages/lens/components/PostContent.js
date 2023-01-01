import ReactMarkdown from "react-markdown";

export default function PostContent({ post }) {
    return (
        <div>
            <h1>{post.metadata.name}</h1>
            <ReactMarkdown>{post.metadata.content}</ReactMarkdown>
        </div>
    )
}