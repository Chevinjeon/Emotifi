import React, { useState } from 'react';
import './ImageGenerator.css';

const ImageGenerator = () => {
    const [imageSrc, setImageSrc] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const fetchGeneratedImage = async ( mood, imgType) => {
        setIsLoading(true);
        const formData = new formData();
        formData.append('mood', mood);
        formData.append('img_type', imgType);

        // Append 'init_img' to formData if modifying an existing image 
        //formData.append('init_img', file); // if imgType is 'modify' 

        try { 
            const response = await fetch('http://localhost:5000/generate-image', {
                method: 'POST', 
                body: formData, 
            });

            if (!response.ok) throw new Error('Network response was not ok.');

            const blob = await response.blob();
            setImageSrc(URL.createObjectURL(blob));
        } catch (error) {
            console.error('Error fetching generate image: ', error);
        } finally { 
            setIsLoading(false);
        }
    };
    

    return (
        <div className='ai-image-generator'>
            <div className="header">Emotion AI <span>Visualization</span></div>
            
                {isLoading ? (
                    <p>Loading...</p>
                )  : (
                    <div className="image">
                        {/* <img src={images[imageIndex]} /> */}
                   </div>
                )}
            <p>This artwork is generated from your brainwave signals:</p>
            <div className="generate-btn" onClick={()=>fetchGeneratedImage('happy', 'abstract')}>Request Image</div>
            <iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1EIgG2NEOhqsD7?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>
    );
};

export default ImageGenerator;
