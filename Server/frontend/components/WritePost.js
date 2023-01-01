import { useForm } from "react-hook-form";
import { useLensContext } from '../context/lensContext';
import {
    createContentMetadata,
    getCreatePostQuery, // Compare to https://github.com/PatrickAlphaC/lens-blog
    lensClient,
  } from "../constants/lensConstants";
import { useWeb3Contract } from "react-moralis";
import lensAbi from '../contracts/lensABI.json';
import {
    lensHub,
    networkConfig,
    TRUE_BYTES,
  } from "../constants/contractConstants";

const PINATA_PIN_ENDPOINT = 'https://api.pinata.cloud/pinning/pinJSONToIPFS';

async function pinMetadataToPinata (
    metadata,
    contentName,
    pinataApiKey,
    pinataApiSecret
) {
    console.log('pinning metadata to pinata');
    const data = JSON.stringify({
        pinataMetadata: { name: contentName },
        pinataContent: metadata,
    });
    const config = {
        method: "POST",
        headers: {
            "Content-Type": 'application/json',
            pinata_api_key: pinataApiKey,
            pinata_secret_api_key: pinataApiSecret,
        },
        body: data,
    };
    const response = await fetch(PINATA_PIN_ENDPOINT, config);
    const ipfsHash = (await response.json()).ipfsHash;
    console.log(`Stored content metadata with ${ipfsHash}`);
    return ipfsHash;
}

function PostForm () {
    const { profileId, token } = useLensContext();
    const { register, errors, handleSubmit, formState, reset, watch } = useForm({
        mode: 'onChange',
    });
    const { runContractFunction } = useWeb3Contract();

    const publishPost = async function ({ content, contentName, imageUri, imageType, pinataApiKey, pinataApiSecret }) {
    let fullContentUri;
    const contentMetadata = createContentMetadata(content, contentName, imageUri, imageType);
    const metadataIpfsHash = await pinMetadataToPinata(contentMetadata, contentName, pinataApiKey, pinataApiSecret);
    fullContentUri = `ipfs://${metadataIpfsHash}`;
    console.log(fullContentUri);

    // Post IPFS hash to Lens/blockchain
    const transactionParameters = [
        profileId,
        fullContentUri,
        '0x23b9467334bEb345aAa6fd1545538F3d54436e96', // Free collect module contract address on Polygon (for now, all posts will be able to be collected without a fee).
        TRUE_BYTES,
        '0x17317F96f0C7a845FFe78c60B10aB15789b57Aaa', // Follower only reference module
    ];
    console.log(transactionParameters);
    const transactionOptions = {
        abi: lensAbi,
        contractAddress: '0xDb46d1Dc155634FbC732f92E853b10B288AD5a1d', // Lens Hub proxy contract address
        functionName: 'post',
        params: {
            vars: transactionParameters,
        },
    };

    await runContractFunction({
        params: transactionOptions,
        onError: (error) => console.log(error),
    });

    return (
        "Hi"
    )
    };

    return (
        <form onSubmit = { handleSubmit( publishPost ) }>
            <input placeholder="Publication title" name='contentName' {...register("contentName", {maxLength: 100, minLength: 1, required: true})} />
            <textarea placeholder="Write your proposal in markdown" name='content' {...register('content', {
                maxLength: 2500, minLength: 10, required: true
            })} />
            <input placeholder="(optional) Image URI" name='imageUri' {...register("imageUri", { // Feature request -> ability to add multiple images? (Markdown ![]() styling as a temporary work around?)
                maxLength: 100, minLength: 1, required: false
            })} />
            <input placeholder="(optional) Image type" name='imageType' {...register("imageType", {
                maxLength: 100, minLength: 1, required: false
            })} />
            <input
                placeholder="(optional) Pinata.cloud API Key"
                name="pinataApiKey"
                {...register("pinataApiKey", { // Feature request -> This should be saved into a user's account (via Supabase) and retrieved whenever this page is loaded
                    maxLength: 100,
                    minLength: 1,
                    required: false,
                })}
            />
            <input
                placeholder="(optional) Pinata.cloud API Secret"
                name="pinataApiSecret"
                {...register("pinataApiSecret", { // Probably would need to implement Moralis <==> Supabase auth process (unless we switch back to Thirdweb SDK for auth & signing) so that the user address is -> Supabase
                    maxLength: 100,
                    minLength: 1,
                    required: false,
                })}
            />
            {errors ? <div>{errors.content?.message}</div> : <div></div> }
            {profileId && token ? (
                <button type='submit'>Publish</button>
            ) : <div>You need to sign in to make a post</div>}
        </form>
    )
}

export default function WritePost () {
    return (
        <div><PostForm /></div>
    )
}

// Send form components to Flask -> Supabase.