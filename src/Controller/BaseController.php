<?php


namespace App\Controller;


use App\Entity\Article;
use JMS\Serializer\SerializerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class BaseController extends AbstractController
{
    public static function getSubscribedServices() {
        return array_merge(parent::getSubscribedServices(), [ 'jms_serializer' => '?'.SerializerInterface::class, ]);
    }
   public function serialize($data){
       $serializer = $this->container->get('jms_serializer');
       return $serializer->serialize($data, 'json');
   }

    public function deserialize($data, $input){
        $serializer = $this->container->get('jms_serializer');
        return $serializer->deserialize($data, $input, "json");
    }

}
