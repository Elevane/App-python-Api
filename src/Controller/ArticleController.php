<?php


namespace App\Controller;
use App\Entity\Article;
use App\Form\ArticleType;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use FOS\RestBundle\Controller\FOSRestController;
use FOS\RestBundle\Controller\Annotations as Rest;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;

/**
 * @Route("/article")
 * @method handleView($view)
 */
class ArticleController extends BaseController
{

    /**
     * @Rest\Get("/list")
     */
    public function listAction(){
        $articles = $this->getDoctrine()->getManager()->getRepository(Article::class)->findAll();
        return $articles;
    }

    /**
     * @Rest\Post("/new")
     * @param Request $request
     * @return JsonResponse
     */
    public function newAction(Request$request){
        $article =new Article();
        $form= $this->createForm(ArticleType::class,$article);
        $data= json_decode($request->getContent(),true);
        $form->submit($data);
        if($form->isSubmitted()&&$form->isValid()){
            $em=$this->getDoctrine()->getManager();
            $em->persist($article);
            $em->flush();
            return new JsonResponse("true");
        }
        return new JsonResponse("false");
    }


    /**
     * @Rest\Delete("/delete/{id}")
     * @param $id
     */
    public function deleteAction($id){
        $em= $this->getDoctrine()->getManager();
        $article = $em->getRepository(Article::class)->findOneBy(array("id"=> $id));
        $em->remove($article);
        $em->flush();

    }

    /**
     * @Rest\Patch("/update")
     * @param Request $request
     * @return JsonResponse
     */
    public function updateAction(Request $request){

            $article = $this->deserialize($request->getContent(), Article::class);
            $em=$this->getDoctrine()->getManager();
            $em->merge($article);
            $em->flush();
            return new JsonResponse("true");

    }

}
